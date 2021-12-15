from tornado.web import (
    RequestHandler,
    HTTPError,
)
from src.models.model import Model
import json


# HTTPError Exceptions.  Should probably be in a module by themselves,
# but I don't want to make this whole thing too complex for what it is.
class BadRequest(HTTPError):
    def __init__(self, *args, **kwargs):
        super().__init__(400, *args, **kwargs)


class AccessCredentialsError(HTTPError):
    def __init__(self, *args, **kwargs):
        super().__init__(400, *args, **kwargs)


class AccessForbiddenError(HTTPError):
    def __init__(self, *args, **kwargs):
        super().__init__(4003, *args, **kwargs)


class NotFoundError(HTTPError):
    def __init__(self, *args, **kwargs):
        super().__init__(404, *args, **kwargs)


class ResourceConflict(HTTPError):
    def __init__(self, *args, **kwargs):
        super().__init__(409, *args, **kwargs)


class CoffeeBrewAttempt(HTTPError):
    def __init__(self, *args, **kwargs):
        super().__init__(418, *args, **kwargs)


def output_json(output):
    def dictify(obj):
        if isinstance(obj, list):
            return [dictify(item) for item in obj]
        elif isinstance(obj, Model):
            return obj.to_dict()
        else:
            return output
    return json.dumps(dictify(output))


class JSONHandler(RequestHandler):
    def initialize(self):
        self.set_header('Content-Type', 'application/json')

    def write_error(self, status_code, **kwargs):
        (exc_type, exc_value, traceback) = \
            kwargs.get('exc_info', (None, None, None))
        if isinstance(exc_value, HTTPError):
            message = exc_value.log_message
        else:
            message = "Server Error"
        self.clear()
        if message is not None:
            self.set_header('Content-Type', 'application/json')
            self.write(output_json({
                'message': message,
            }))
        self.set_status(status_code)

    def get_json_request(self):
        try:
            return json.loads(self.request.body)
        except Exception:
            raise BadRequest('Invalid request payload')


class DefaultHandler(JSONHandler):
    def get(self):
        raise NotFoundError()
