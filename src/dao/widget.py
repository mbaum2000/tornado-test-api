from .base import DAO
from src.models.widget import Widget


class WidgetDAO(DAO):
    def list_widgets(self):
        sql = """
            SELECT
                id,
                name,
                parts,
                created,
                updated
            FROM widgets
        """

        result = self.engine.execute(sql)
        rows = result.fetchall()

        return [Widget.from_row(row) for row in rows]

    def get_widget(self, id):
        sql = """
            SELECT
                id,
                name,
                parts,
                created,
                updated
            FROM widgets
            WHERE id = :id
        """

        result = self.engine.execute(sql, {
            'id': id
        })
        row = result.fetchone()
        if row is None:
            return None

        return Widget.from_row(row)

    def update_widget(self, widget):
        sql = """
            UPDATE widgets
            SET
                name = :name,
                parts = :parts,
                updated = DATETIME('now')
            WHERE id = :id
        """

        self.engine.execute(sql, {
            'id': widget.id,
            'name': widget.name,
            'parts': widget.parts,
        })

    def create_widget(self, widget):
        sql = """
            INSERT INTO widgets
                (name, parts, created, updated)
            VALUES
                (:name, :parts, DATETIME('now'), DATETIME('now'))
        """

        result = self.engine.execute(sql, {
            'name': widget.name,
            'parts': widget.parts,
        })
        return result.lastrowid

    def delete_widget(self, id):
        sql = """
            DELETE FROM widgets
            WHERE id = :id
        """

        self.engine.execute(sql, {
            'id': id,
        })
