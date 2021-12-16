from tornado.web import (
    MissingArgumentError,
)
from src.dao.base import (
    get_engine,
    get_default_db_file,
)
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


class WidgetsHandler(JSONHandler):
    def initialize(self):
        super().initialize()
        self.dao = WidgetDAO(engine=get_engine(get_default_db_file()))

    def get(self):
        # TODO: Add Pagination
        try:
            widgets = self.dao.list_widgets()
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
            try:
                parts = int(parts)
            except ValueError:
                raise BadRequest(
                    'Invalid argument: parts is not a number'
                )
            if parts < 0:
                raise BadRequest(
                    'Invalid argument: parts must not be negative'
                )

            widget = Widget(
                name=name,
                parts=parts,
            )
            id = self.dao.create_widget(widget)
            widget = self.dao.get_widget(id)
            self.write(output_json(widget))

        except IntegrityError:
            raise ResourceConflict(f"A Widget with name '{name}' exists")
        except Exception:
            raise


class WidgetHandler(JSONHandler):
    def initialize(self):
        super().initialize()
        self.dao = WidgetDAO(engine=get_engine(get_default_db_file()))

    def get(self, id):
        try:
            widget = self.dao.get_widget(id)
            if widget is None:
                raise NotFoundError(f"A Widget with id '{id}' was not found")
            self.write(output_json(widget))
        except Exception:
            raise

    def put(self, id):
        try:
            widget = self.dao.get_widget(id)
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
            try:
                parts = int(parts)
            except ValueError:
                raise BadRequest(
                    'Invalid argument: parts is not a number'
                )
            if parts < 0:
                raise BadRequest(
                    'Invalid argument: parts must not be negative'
                )

            widget.name = name
            widget.parts = parts

            self.dao.update_widget(widget)
            widget = self.dao.get_widget(id)

            self.write(output_json(widget))

        except IntegrityError:
            raise ResourceConflict(f"A Widget with name '{name}' exists")
        except Exception:
            raise

    def delete(self, id):
        try:
            widget = self.dao.get_widget(id)
            if widget is None:
                raise NotFoundError(f"A Widget with id '{id}' was not found")
            self.dao.delete_widget(id)
            self.set_status(204)
        except Exception:
            raise
