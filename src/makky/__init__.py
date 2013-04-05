import os
import urlparse
from webob.dec import wsgify
from webob.exc import HTTPFound
from mako.lookup import TemplateLookup
from mako.template import Template

class Makky(object):
    def __init__(self, root, directories):
        self.root = root
        self.directories = directories
        self.templates = TemplateLookup(directories=directories)

    @wsgify
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

        return tmpl.render(request=request)

def main(global_conf, root, directories=[], **app_conf):
    app = Makky(root=root, directories=directories)
    return app
