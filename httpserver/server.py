

class HTTPServer:

    def __init__(self, host="localhost", port=8080):
        self.host = host
        self.port = port

    def run_forever(self):
        print("Running the server on {}:{}".format(self.host, self.port))
        pass
