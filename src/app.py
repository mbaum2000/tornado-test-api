from tornado.web import Application
from src.handlers.widget import (
    WidgetsHandler,
    WidgetHandler,
)
from src.handlers.base import (
    DefaultHandler,
)
import os


def make_app():
    # TODO: Would be AWesome to dynamically load these via a decorator
    handlers = [
        (r"/", DefaultHandler),
        (r"/widget", WidgetsHandler),
        (r"/widget/([^/]+)?", WidgetHandler),
    ]
    debug = os.environ.get('DEBUG', '0') == '1'
    app = Application(handlers=handlers, debug=debug)
    port = int(os.environ.get('PORT', 8080))
    app.listen(port)
    return app
