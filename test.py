import os
import sqlite3
import unittest
from fastapi.testclient import TestClient

from main import  app, create_table, increment_count, DB_FILE

class FastAPITest(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)
        self.db_file = DB_FILE
        create_table()

    def tearDown(self):
        conn = sqlite3.connect(self.db_file)
        conn.execute("DROP TABLE IF EXISTS access_count")
        conn.commit()
        conn.close()

    def test_example_endpoint(self):
        response = self.client.get("/example")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "¡Hola! Has accedido al endpoint /example."})

        conn = sqlite3.connect(self.db_file)
        c = conn.cursor()
        c.execute("SELECT count FROM access_count WHERE endpoint = 'example'")
        result = c.fetchone()
        conn.close()

        self.assertEqual(result[0], 1)

    def test_count_endpoint(self):
        increment_count("test_endpoint")

        response = self.client.get("/count/test_endpoint")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"endpoint": "test_endpoint", "count": 1})

    def test_count_endpoint_not_found(self):
        response = self.client.get("/count/nonexistent_endpoint")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"endpoint": "nonexistent_endpoint", "count": 0})

if __name__ == '__main__':
    unittest.main()