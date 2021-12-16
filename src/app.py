from tornado.web import Application
from src.handlers.widget import (
    WidgetsHandler,
    WidgetHandler,
)
from src.handlers.base import (
    DefaultHandler,
)
import os
from src.dao.base import set_default_db_file


def make_app(db_filename=None):
    if db_filename is not None:
        set_default_db_file(db_filename)

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
