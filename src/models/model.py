from datetime import datetime


class Model(object):
    def __init__(self, **kwargs):
        for name, value in kwargs.items():
            if hasattr(self, name):
                setattr(self, name, value)

    @classmethod
    def from_row(cls, row):
        model = cls()
        for name, value in zip(row.keys(), row):
            if hasattr(model, name):
                setattr(model, name, value)
        return model

    def to_dict(self):
        result = {}
        for name, value in self.__dict__.items():
            if isinstance(value, datetime):
                value = value.strftime('%Y-%m-%d %H:%M:%S')
            result[name] = value
        return result
