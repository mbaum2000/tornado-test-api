from tornado.web import (
    MissingArgumentError,
)
from src.dao.base import get_engine
from src.dao.widget import WidgetDAO
from src.models.widget import Widget
from sqlalchemy.exc import (
    IntegrityError
)
from .base import (
    JSONHandler,
    output_json,
    BadRequest,
    NotFoundError,
    ResourceConflict,
)
import os


# The DB_FILENAME should probably be defined in the app itself.
db_file = os.environ.get('DB_FILENAME', 'sqlite:///widgets.db')
dao = WidgetDAO(engine=get_engine(db_file))


class WidgetsHandler(JSONHandler):
    def get(self):
        try:
            widgets = dao.list_widgets()
            self.write(output_json(widgets))
        except Exception:
            raise

    def post(self):
        try:
            data = self.get_json_request()

            name = data.get('name')
            if name is None:
                raise MissingArgumentError("'name'")
            if len(name) > Widget.MAX_NAME_LEN:
                raise BadRequest(
                    f'Invalid argument: name is greater than {Widget.MAX_NAME_LEN} characters'  # noqa: E501
                )

            parts = data.get('parts')
            if parts is None:
                raise MissingArgumentError("'parts'")

            widget = Widget(
                name=name,
                parts=parts,
            )
            id = dao.create_widget(widget)
            widget = dao.get_widget(id)
            self.write(output_json(widget))

        except IntegrityError:
            raise ResourceConflict(f"A Widget with name '{name}' exists")
        except Exception:
            raise


class WidgetHandler(JSONHandler):
    def initialize(self):
        self.set_header('Content-Type', 'application/json')

    def get(self, id):
        try:
            widget = dao.get_widget(id)
            if widget is None:
                raise NotFoundError(f"A Widget with id '{id}' was not found")
            self.write(output_json(widget))
        except Exception:
            raise

    def put(self, id):
        try:
            widget = dao.get_widget(id)
            if widget is None:
                raise NotFoundError(f"A Widget with id '{id}' was not found")

            data = self.get_json_request()

            name = data.get('name')
            if name is None:
                raise MissingArgumentError("'name'")
            if len(name) > Widget.MAX_NAME_LEN:
                raise BadRequest(
                    f'Invalid argument: name is greater than {Widget.MAX_NAME_LEN} characters'  # noqa: E501
                )

            parts = data.get('parts')
            if parts is None:
                raise MissingArgumentError("'parts'")

            widget.name = name
            widget.parts = parts

            dao.update_widget(widget)
            widget = dao.get_widget(id)

            self.write(output_json(widget))

        except IntegrityError:
            raise ResourceConflict(f"A Widget with name '{name}' exists")
        except Exception:
            raise

    def delete(self, id):
        try:
            widget = dao.get_widget(id)
            if widget is None:
                raise NotFoundError(f"A Widget with id '{id}' was not found")
            dao.delete_widget(id)
            self.set_status(204)
        except Exception:
            raise
