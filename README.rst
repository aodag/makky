Makky
================

Makky is mako template application like PHP.


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
    use = egg:makky
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



It's wsgi application. 
You can run this application with ``gearbox serve``::

    $ gearbox serve app.ini
