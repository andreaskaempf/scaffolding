# scaffolding
Basic scaffolding for a web application, using CherryPy

To use this, you need to install CherryPy:

pip install cherrypy

You should also download Bootstrap version 3 from http://getbootstrap.com, 
and install it in static/bootstrap3. Of course, you can upgrade to a later
version of Bootstrap.

The main file app.py contains boilerplate code to create a simple 3-page
web app, with a menu along the top. You can rename, add, or remove pages
by changing the function definitions inside the Main class.

There is no templating -- use any template engine you like. Also, there
is no database or object-relational mapper. Again, use any you like.

To run the application:

python3 app.py

You can then browse to http://localhost:8000

Note that nested static file serving (e.g., bootstrap linked from the
header.html file) seems to be very slow, due to a bug. In general, it is
best to run CherryPy (and any Python web server) behind a web server such
as Nginx, lighttpd, or Apache. Instructions and a config file will follow.

To do:
- Config file for running behind server
- User log ins
- Administration page to manage users
