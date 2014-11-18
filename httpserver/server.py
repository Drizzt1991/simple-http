from wsgiref.simple_server import make_server


class HTTPServer:

    def __init__(self, host="127.0.0.1", port=8085):
        self.host = host
        self.port = port

    def hello_world_app(self, environ, start_response):
        status = '200 OK'  # HTTP Status
        headers = [('Content-type', 'text/plain; charset=utf-8')]
        start_response(status, headers)

        # The returned object is going to be printed
        return [b"Hello World"]

    def run_forever(self):
        print("Running the server on {}:{}".format(self.host, self.port))

        # Every WSGI application must have an application object - a callable
        # object that accepts two arguments. For that purpose, we're going to
        # use a function (note that you're not limited to a function, you can
        # use a class for example). The first argument passed to the function
        # is a dictionary containing CGI-style envrironment variables and the
        # second variable is the callable object (see PEP 333).
        httpd = make_server(self.host, self.port, self.hello_world_app)
        # Serve until process is killed
        httpd.serve_forever()
