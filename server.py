# encoding: utf-8
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
from .view import WebHandler
from . import USER_AGENT, LOG


class Server(HTTPServer):
    """
    Python native WebServer
    """
    def __init__(self, ip, port, datastore):
        self.datastore = datastore
        self.view = WebHandler(datastore)
        HTTPServer.__init__(self, (ip, port), HttpRequestHandler)
        LOG.info('Server started on %s:%s using datastore %s', ip, port,
                 type(datastore))


class HttpRequestHandler(BaseHTTPRequestHandler):
    """ RequestHandler wrap to WebHandler """

    @property
    def view(self):
        return self.server.view

    def version_string(self):
        return USER_AGENT

    def from_response(self, response):
        if response.status == 404:
            self.send_error(404, 'Not Found')
        else:
            self.send_response(response.status)
        self.send_header('Content-type', response.mimetype)
        if not (response.content is None):
            self.send_header('Content-Length', len(response.content))
        self.end_headers()
        if not (response.content is None):
            self.wfile.write(response.content)

    def do_HEAD(self):
        self.from_response(self.view.head(self.path))

    def do_GET(self):
        self.from_response(self.view.get(self.path))

    def do_POST(self):
        self.from_response(self.view.post(self.path))

    def log_message(self, format, *args):
        # use python logging
        LOG.info("%s - %s" % (self.client_address[0], format % args))
