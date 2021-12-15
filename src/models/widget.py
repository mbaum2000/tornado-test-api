from .model import Model


class Widget(Model):
    MAX_NAME_LEN = 64

    def __init__(self, **kwargs):
        self.id = None
        self.name = None
        self.parts = None
        self.created = None
        self.updated = None
        super().__init__(**kwargs)
