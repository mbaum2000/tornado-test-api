from sqlalchemy import create_engine
import os


engines = {}


def get_engine(filename):
    if filename not in engines:
        echo = os.environ.get('DEBUG_SQL', '0') == '1'
        engines[filename] = create_engine(filename, echo=echo)
    return engines[filename]


class DAO:
    def __init__(self, engine):
        self.engine = engine
        self.init_db()

    def init_db(self):
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
        self.engine.execute(schema)
