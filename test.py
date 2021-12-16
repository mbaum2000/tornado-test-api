from tornado.testing import AsyncHTTPTestCase
from src.app import make_app
from src.dao.base import get_engine
import json


class TestWidgetApp(AsyncHTTPTestCase):
    def get_app(self):
        db_file = 'sqlite:///:memory:'
        app = make_app(db_filename=db_file)
        engine = get_engine(db_file)

        # For each test, wipe the db clean
        engine.execute("""
            DELETE FROM widgets;
        """)
        # Reset autoincrement for consistency
        engine.execute("""
            UPDATE `sqlite_sequence`
            SET `seq` = 0
            WHERE `name` = 'widgets';
        """)
        # And fill with sample data
        engine.execute("""
            INSERT INTO widgets
                (`name`, `parts`, `created`, `updated`)
            VALUES
                ('foo', 2, '2021-12-14 23:01:35', '2021-12-14 23:01:35'),
                ('bar', 1, '2021-12-14 23:09:06', '2021-12-14 23:09:06'),
                ('baz', 9, '2021-12-14 23:26:24', '2021-12-14 23:26:24');
        """)
        return app

    def test_list(self):
        response = self.fetch('/widget', method='GET')
        self.assertEqual(response.code, 200)
        json_response = json.loads(response.body)
        self.assertIsInstance(json_response, list)
        self.assertEqual(len(json_response), 3)
        first_item = json_response[0]
        self.assertIsInstance(first_item, dict)
        self.assertIn('id', first_item)
        self.assertEqual(first_item['id'], 1)
        self.assertIn('name', first_item)
        self.assertEqual(first_item['name'], 'foo')
        self.assertIn('parts', first_item)
        self.assertEqual(first_item['parts'], 2)
        self.assertIn('created', first_item)
        self.assertEqual(first_item['created'], '2021-12-14 23:01:35')
        self.assertIn('updated', first_item)
        self.assertEqual(first_item['updated'], '2021-12-14 23:01:35')

    def test_get(self):
        response = self.fetch('/widget/1', method='GET')
        self.assertEqual(response.code, 200)
        json_response = json.loads(response.body)
        self.assertIsInstance(json_response, dict)
        self.assertIn('id', json_response)
        self.assertEqual(json_response['id'], 1)
        self.assertIn('name', json_response)
        self.assertEqual(json_response['name'], 'foo')
        self.assertIn('parts', json_response)
        self.assertEqual(json_response['parts'], 2)
        self.assertIn('created', json_response)
        self.assertEqual(json_response['created'], '2021-12-14 23:01:35')
        self.assertIn('updated', json_response)
        self.assertEqual(json_response['updated'], '2021-12-14 23:01:35')

    def test_get_not_exist(self):
        response = self.fetch('/widget/4', method='GET')
        self.assertEqual(response.code, 404)
        json_response = json.loads(response.body)
        self.assertIsInstance(json_response, dict)
        self.assertIn('message', json_response)

    def test_put(self):
        response = self.fetch('/widget/1', method='PUT', body=json.dumps({
            'name': 'blarg',
            'parts': 3,
        }))
        self.assertEqual(response.code, 200)
        json_response = json.loads(response.body)
        self.assertIsInstance(json_response, dict)
        self.assertIn('id', json_response)
        self.assertEqual(json_response['id'], 1)
        self.assertIn('name', json_response)
        self.assertEqual(json_response['name'], 'blarg')
        self.assertIn('parts', json_response)
        self.assertEqual(json_response['parts'], 3)
        self.assertIn('created', json_response)
        self.assertEqual(json_response['created'], '2021-12-14 23:01:35')
        self.assertIn('updated', json_response)
        self.assertGreater(json_response['updated'], '2021-12-14 23:01:35')

    def test_put_not_exist(self):
        response = self.fetch('/widget/4', method='PUT', body=json.dumps({
            'name': 'blarg',
            'parts': 3,
        }))
        self.assertEqual(response.code, 404)
        json_response = json.loads(response.body)
        self.assertIsInstance(json_response, dict)
        self.assertIn('message', json_response)

    def test_put_duplicate(self):
        response = self.fetch('/widget/1', method='PUT', body=json.dumps({
            'name': 'bar',
            'parts': 3,
        }))
        self.assertEqual(response.code, 409)
        json_response = json.loads(response.body)
        self.assertIsInstance(json_response, dict)
        self.assertIn('message', json_response)

    def test_put_missing_arg_name(self):
        response = self.fetch('/widget/1', method='PUT', body=json.dumps({
            'parts': 3,
        }))
        self.assertEqual(response.code, 400)
        json_response = json.loads(response.body)
        self.assertIsInstance(json_response, dict)
        self.assertIn('message', json_response)

    def test_put_invalid_arg_name(self):
        response = self.fetch('/widget/1', method='PUT', body=json.dumps({
            'name': ('x' * 65),
            'parts': 3,
        }))
        self.assertEqual(response.code, 400)
        json_response = json.loads(response.body)
        self.assertIsInstance(json_response, dict)
        self.assertIn('message', json_response)

    def test_put_missing_arg_parts(self):
        response = self.fetch('/widget/1', method='PUT', body=json.dumps({
            'name': 'blarg',
        }))
        self.assertEqual(response.code, 400)
        json_response = json.loads(response.body)
        self.assertIsInstance(json_response, dict)
        self.assertIn('message', json_response)

    def test_put_invalid_arg_parts_str(self):
        response = self.fetch('/widget/1', method='PUT', body=json.dumps({
            'name': 'blarg',
            'parts': 'three',
        }))
        self.assertEqual(response.code, 400)
        json_response = json.loads(response.body)
        self.assertIsInstance(json_response, dict)
        self.assertIn('message', json_response)

    def test_put_invalid_arg_parts_neg(self):
        response = self.fetch('/widget/1', method='PUT', body=json.dumps({
            'name': 'blarg',
            'parts': -1,
        }))
        self.assertEqual(response.code, 400)
        json_response = json.loads(response.body)
        self.assertIsInstance(json_response, dict)
        self.assertIn('message', json_response)

    def test_post(self):
        response = self.fetch('/widget', method='POST', body=json.dumps({
            'name': 'blarg',
            'parts': 3,
        }))
        self.assertEqual(response.code, 200)
        json_response = json.loads(response.body)
        self.assertIsInstance(json_response, dict)
        self.assertIn('id', json_response)
        self.assertEqual(json_response['id'], 4)
        self.assertIn('name', json_response)
        self.assertEqual(json_response['name'], 'blarg')
        self.assertIn('parts', json_response)
        self.assertEqual(json_response['parts'], 3)
        self.assertIn('created', json_response)
        self.assertGreater(json_response['created'], '2021-12-14 23:01:35')
        self.assertIn('updated', json_response)
        self.assertGreater(json_response['updated'], '2021-12-14 23:01:35')

    def test_post_utf8_name(self):
        response = self.fetch('/widget', method='POST', body=json.dumps({
            'name': 'ひらがな',
            'parts': 3,
        }))
        self.assertEqual(response.code, 200)
        json_response = json.loads(response.body)
        self.assertIsInstance(json_response, dict)
        self.assertIn('id', json_response)
        self.assertEqual(json_response['id'], 4)
        self.assertIn('name', json_response)
        self.assertEqual(json_response['name'], 'ひらがな')
        self.assertIn('parts', json_response)
        self.assertEqual(json_response['parts'], 3)
        self.assertIn('created', json_response)
        self.assertGreater(json_response['created'], '2021-12-14 23:01:35')
        self.assertIn('updated', json_response)
        self.assertGreater(json_response['updated'], '2021-12-14 23:01:35')

    def test_post_duplicate(self):
        response = self.fetch('/widget', method='POST', body=json.dumps({
            'name': 'foo',
            'parts': 3,
        }))
        self.assertEqual(response.code, 409)
        json_response = json.loads(response.body)
        self.assertIsInstance(json_response, dict)
        self.assertIn('message', json_response)

    def test_post_missing_arg_name(self):
        response = self.fetch('/widget', method='POST', body=json.dumps({
            'parts': 3,
        }))
        self.assertEqual(response.code, 400)
        json_response = json.loads(response.body)
        self.assertIsInstance(json_response, dict)
        self.assertIn('message', json_response)

    def test_post_invalid_arg_name(self):
        response = self.fetch('/widget', method='POST', body=json.dumps({
            'name': ('x' * 65),
            'parts': 3,
        }))
        self.assertEqual(response.code, 400)
        json_response = json.loads(response.body)
        self.assertIsInstance(json_response, dict)
        self.assertIn('message', json_response)

    def test_post_missing_arg_parts(self):
        response = self.fetch('/widget', method='POST', body=json.dumps({
            'name': 'blarg',
        }))
        self.assertEqual(response.code, 400)
        json_response = json.loads(response.body)
        self.assertIsInstance(json_response, dict)
        self.assertIn('message', json_response)

    def test_post_invalid_arg_parts_str(self):
        response = self.fetch('/widget', method='POST', body=json.dumps({
            'name': 'blarg',
            'parts': 'three',
        }))
        self.assertEqual(response.code, 400)
        json_response = json.loads(response.body)
        self.assertIsInstance(json_response, dict)
        self.assertIn('message', json_response)

    def test_post_invalid_arg_parts_neg(self):
        response = self.fetch('/widget', method='POST', body=json.dumps({
            'name': 'blarg',
            'parts': -1,
        }))
        self.assertEqual(response.code, 400)
        json_response = json.loads(response.body)
        self.assertIsInstance(json_response, dict)
        self.assertIn('message', json_response)

    def test_delete(self):
        response = self.fetch('/widget/1', method='DELETE')
        self.assertEqual(response.code, 204)
        response = self.fetch('/widget/1', method='GET')
        self.assertEqual(response.code, 404)

    def test_delete_not_exist(self):
        response = self.fetch('/widget/4', method='DELETE')
        self.assertEqual(response.code, 404)
        json_response = json.loads(response.body)
        self.assertIsInstance(json_response, dict)
        self.assertIn('message', json_response)
