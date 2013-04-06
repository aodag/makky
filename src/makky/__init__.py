import os
import urlparse
import paginate
from beaker.middleware import SessionMiddleware
from webob import Request
from webob.dec import wsgify
from webob.exc import HTTPFound, HTTPNotFound
from mako.lookup import TemplateLookup
from mako.template import Template
try:
    import psycopg2
except ImportError:
    has_psycopg2 = False
else:
    has_psycopg2 = True

from . import helpers

class MakkyRequest(Request):
    @property
    def session(self):
        return self.environ['beaker.session']

class DB(object):
    def __init__(self, dsn):
        self.dsn = dsn

    def connect(self):
        return psycopg2.connect(self.dsn)

class Makky(object):
    def __init__(self, root, directories, dsn=None):
        self.root = root
        self.directories = directories
        self.templates = TemplateLookup(directories=directories)
        self.db = None
        if dsn:
            if not has_psycopg2:
                raise Exception("dsn is specified, but psycopg2 is not installed.")

            self.db = DB(dsn)


    @wsgify(RequestClass=MakkyRequest)
    def __call__(self, request):

        if not request.path_info:
            path = "index.html"
        elif request.path_info.endswith("/"):
            path = request.path_info + "index.html"
        else:
            path = request.path_info

        if path.startswith("/"):
            path = path[1:]

        path = os.path.abspath(os.path.normpath(os.path.join(self.root, path)))
        if not os.path.exists(path):
            return HTTPNotFound()

        if os.path.isdir(path):
            parts = urlparse.urlparse(request.url)
            parts = urlparse.ParseResult(scheme=parts.scheme,
                                         netloc=parts.netloc,
                                         path=parts.path + "/",
                                         params=parts.params,
                                         query=parts.query,
                                         fragment=parts.fragment)
            location = urlparse.urlunparse(parts)
            return HTTPFound(location=location)

        tmpl = Template(filename=path,
                        lookup=self.templates)

        return tmpl.render(request=request,
                           h=helpers,
                           paginate=paginate,
                           db=self.db)


truthy = frozenset(['true', 'yes', 'on', 'y', 't', '1'])
falsy = frozenset(['false', 'no', 'off', 'n', 'f', '0'])


def asbool(obj):
    if isinstance(obj, basestring):
        obj = obj.strip().lower()
        if obj in truthy:
            return True
        elif obj in falsy:
            return False
        else:
            raise ValueError("String is not true/false: %r" % obj)
    return bool(obj)

def main(global_conf, root, directories=[], dsn=None, **app_conf):
    debug = asbool(app_conf.get('debug'))
    app = Makky(root=root, directories=directories, dsn=dsn)
    app = SessionMiddleware(app, app_conf)
    if debug:
        import backlash
        app = backlash.DebuggedApplication(app)
    return app
