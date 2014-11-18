from .server import HTTPServer


def main():
    srv = HTTPServer()
    srv.run_forever()


if __name__ == "__main__":
    main()
