import socket
import time

import threading
import random

from concurrent.futures import ThreadPoolExecutor


# class ThreadPool:

#     def __init__(self, n_threads):
#         self.n_threads = n_threads
#         self.queue = Queue(n_threads)
#         self.threads = []

#     def process(self, func, args):
#         self.queue.put((func, args))

#         self.threads = [x for x in self.threads if x.is_alive()]

#         if len(self.threads) < self.n_threads:
#             thread = threading.Thread(target=self._process_queue)
#             thread.start()
#             self.threads.append(thread)

#     def _process_queue(self):
#         while not self.queue.empty():
#             func, args = self.queue.get()
#             func(*args)


class HTTPServer:

    def __init__(self, host="127.0.0.1", port=8085):
        self.host = host
        self.port = port
        self._pool = ThreadPoolExecutor(max_workers=100)

    def run_forever(self):
        # Create socket. Not bound yet.
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Add this so we can restart it multiple times. Is not availible on Win
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        print('Bind on host {} and port {}'.format(self.host, self.port))
        self.socket.bind((self.host, self.port))

        self.socket.listen(100)

        try:
            self._start_receiving()
        except KeyboardInterrupt:
            self._pool.shutdown()
            raise

    def _start_receiving(self):
        while True:
            conn, addr = self.socket.accept()

            self._pool.submit(self._process, conn, addr)

    def _process(self, conn, addr):

            print("Start connection", addr)

            data = conn.recv(1024)
            data = data.decode('ascii')

            #print('Received', data)
            first_line, headers = data.split('\n')[0], data.split('\n')[1:]
            method, path, http_type = first_line.split(' ')

            time.sleep(10*random.random())

            if method == "GET":
                if path == "/":
                    response = ("200 OK", "Hello world")
                else:
                    response = ("200 OK", "Hello {}".format(path))

            else:
                response = ("405 Method Not Allowed", "Error")

            resp = [
                "HTTP/1.1 {}".format(response[0]),
                "Date: Wed, 11 Feb 2009 11:20:59 GMT",
                "Server: Apache",
                "X-Powered-By: PHP/5.2.4-2ubuntu5wm1",
                "Last-Modified: Wed, 11 Feb 2009 11:20:59 GMT",
                "Content-Language: ru",
                "Content-Type: text/html; charset=utf-8",
                "Content-Length: {}".format(len(response[1])),
                "Connection: close",
                "",
                response[1]
            ]

            resp = '\n'.join(resp)

            # print('RESPONSE: \n', resp)

            resp = resp.encode('ascii')

            conn.sendall(resp)

            conn.close()
