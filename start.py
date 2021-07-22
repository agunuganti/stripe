from sanic.server import HttpProtocol

from services.app import app


def runserver(host, port):
    app.run(host=host, port=port, protocol=HttpProtocol)

if __name__ == "__main__":
    runserver("localhost", 5000)