#!/usr/bin/env python3

from tornado.ioloop import IOLoop
from src.app import make_app


if __name__ == '__main__':
    app = make_app()
    IOLoop.instance().start()
