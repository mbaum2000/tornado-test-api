from sqlalchemy import create_engine
import os


engines = {}
config = {
    'default_db_file': os.environ.get(
        'DB_FILENAME',
        'sqlite:///widgets.db'
    ),
}


def get_default_db_file():
    return config.get('default_db_file')


def set_default_db_file(filename):
    config['default_db_file'] = filename


def get_engine(filename):
    if filename not in engines:
        echo = os.environ.get('DEBUG_SQL', '0') == '1'
        engine = create_engine(filename, echo=echo)
        engines[filename] = engine
        DAO.init_db(engine)
    return engines[filename]


class DAO:
    def __init__(self, engine):
        self.engine = engine

    @staticmethod
    def init_db(engine):
        # Ideally, this would not be in the application, but would be
        # administered independently.  However, to simplify the startup
        # of this sample app, it will be run here.
        schema = """
            CREATE TABLE IF NOT EXISTS `widgets` (
                `id` INTEGER PRIMARY KEY AUTOINCREMENT,
                `name` VARCHAR(64) NOT NULL,
                `parts` UNSIGNED INTEGER NOT NULL,
                `created` DATETIME NOT NULL,
                `updated` DATETIME NOT NULL,
                UNIQUE(`name`)
            );
        """
        engine.execute(schema)
