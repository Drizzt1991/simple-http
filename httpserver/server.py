from wsgiref.simple_server import make_server
from .blog import app


class HTTPServer:

    def __init__(self, host="127.0.0.1", port=8085):
        self.host = host
        self.port = port

    def run_forever(self):
        httpd = make_server(self.host, self.port, app)
        print("Serving on port {}...".format(self.port))

        # Serve until process is killed
        httpd.serve_forever()
