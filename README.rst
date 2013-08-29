Makky
================

Makky is mako template application like PHP.

.. contents::


INSTALL
----------------------

::

    $ pip install makky


USAGE
----------------------

Create your application directory and put ``app.ini`` ::

    [app:main]
    use = egg:makky
    root = %(here)s/app

    [server:main]
    use = egg:gunicorn#main
    host = 0.0.0.0
    port = 8888



Create ``app`` directory to your application directory.
And put the template file named ``index.html`` to ``app`` directory::

    <html>
    <%
    message = "Hello"
    %>
      <body>
        <h1>${message}</h1>
      </body>
    </html>

The template uses syntax of `Mako <http://www.makotemplates.org>`_.

Application directory structure::

   yourapp
   ├─ app.ini
   └─ app
       └─ index.html
   

It's wsgi application. 
You can run this application with ``gearbox serve``::

    $ gearbox serve -c app.ini


CONFIG
----------------------

debug
  if true, enable web debugger of ``backlash``.

static
   specify static directories with mount names.


VARIABLES
--------------------------

In template, you can use the variables such as below:

request
  request object of ``WebOb``.

request.session
  http session of ``Beaker``

paginate
  pagienate

h
  helpers of ``WebHelpers2``

