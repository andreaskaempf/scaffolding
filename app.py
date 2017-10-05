#!/bin/python3
#
# Basic scaffolding for a Python web application, using CherryPy
#
# Based on many applications developed by Andreas Kaempf and Soundience,
# 2008 through 2017.
#
# Andreas Kaempf, 1/10/2017


import os, socket
from io import StringIO
import cherrypy as cp

# Configuration settings
banner = 'My Application'		# Appears in menu
menu = ['home', 'page1', 'page2']	# Menu, each name a page
port = 8000				# Web server port
workstations = ['shuttle', 'zenbook']	# Host names not here are considered servers


# This class contains the handlers for web pages. Add more pages by
# creating another def with same arguments and the @cp.expose line
# before it. Each function must return a string. Using StringIO() because
# it is fast, but building up any string is fine.
class Main:

    # Default page redirects to first item in menu
    @cp.expose
    def index(self, **args):
        raise cp.HTTPRedirect('/' + menu[0])

    # Home page
    @cp.expose
    def home(self, **args):

        s = StringIO()
        header(s, 'home')
        s.write('<h1>Home</h1>\n')
        footer(s)
        return s.getvalue()

    # Another page
    @cp.expose
    def page1(self, **args):
        s = StringIO()
        header(s, 'page1')
        s.write('<h1>Page 1</h1>\n')
        footer(s)
        return s.getvalue()

    # And another
    @cp.expose
    def page2(self, **args):
        s = StringIO()
        header(s, 'page2')
        s.write('<h1>Page 2</h1>\n')
        footer(s)
        return s.getvalue()


# Start a new page, with current menu selection highlighted. Most of
# the heading HTML is contained in static/header.html, but the menu
# and start of the main container is here.
def header(s, current):

    # Basic header stuff. If there is no current menu selection,
    # don't go any furtehr.
    s.write(open('static/header.html').read())
    if not current:
        return

    # Navigation bar
    s.write('<nav class="navbar navbar-default">\n')
    s.write('<div class="container-fluid">\n')

    # Navbar header (just site name for now)
    s.write('<div class="navbar-header">\n')
    s.write('  <a class="navbar-brand" href="/%s">%s</a>\n' % (menu[0], banner))
    s.write('</div>\n')

    # Menu links
    s.write('<ul class="nav navbar-nav">\n')
    for m in menu:
        #c = 'class="active"' if m == current else ''  #BOOTSTRAP ACTIVE CLASS NOT WORKING
        c = 'style="background-color: #eee"' if m == current else ''
        s.write('<li %s><a href="/%s">%s</a></li>\n' % (c, m, m.title()))
    s.write('</ul>\n')

    # End of navigation bar
    s.write('</nav>\n')

    # Content div
    s.write('<div class="container">\n')


# Finish page
def footer(s):
    s.write(open('static/footer.html').read())


# Global settings for CherryPy
globalSettings = { 'server.socket_port' : port }
globalSettings['log.screen'] = socket.gethostname() in workstations
globalSettings['log.error_file'] = '/tmp/app.err'
globalSettings['access_log.filename'] = '/tmp/app.log'

# Different settings for workstation vs. production
if socket.gethostname() in workstations:
    globalSettings['server.thread_pool'] = 1
else:
    globalSettings['environment'] = 'production'
    globalSettings['server.thread_pool'] = 4

# Application settings: enable file-based sessions
appSettings = {}
appSettings['/'] = {
    'tools.sessions.on'             : True,
    'tools.sessions.storage_type'   : 'File',
    'tools.sessions.storage_path'   : '/tmp',
    'tools.sessions.timeout'        : 30
}

# Warning: staticdir is very slow if a staticfile links to another static file,
# run behind a web server like nginx or lighttpd if possible
appSettings['/static'] = {
    'tools.staticdir.on' : True,
    'tools.staticdir.dir' : os.getcwd() + '/static'
}

# Start server
cp.config.update(globalSettings)
cp.quickstart(Main(), config = appSettings)

