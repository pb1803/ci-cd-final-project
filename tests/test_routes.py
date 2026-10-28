"""Tests for the counter service API."""

from unittest import TestCase

from service.common import status
from service.routes import app, reset_counters


class CounterTest(TestCase):
    """Exercise the counter REST API."""

    @classmethod
    def setUpClass(cls):
        app.testing = True

    def setUp(self):
        reset_counters()
        self.client = app.test_client()

    def test_index(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.get_json()["message"], "Hit Counter Service")

    def test_health(self):
        response = self.client.get("/health")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.get_json(), {"status": "OK"})

    def test_create_counter(self):
        response = self.client.post("/counters/foo")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.get_json(), {"name": "foo", "counter": 0})
        self.assertIn("/counters/foo", response.headers["Location"])

    def test_create_duplicate_counter(self):
        self.client.post("/counters/foo")
        response = self.client.post("/counters/foo")
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)

    def test_list_counters(self):
        self.assertEqual(self.client.get("/counters").get_json(), [])
        self.client.post("/counters/foo")
        self.assertEqual(
            self.client.get("/counters").get_json(),
            [{"name": "foo", "counter": 0}],
        )

    def test_read_counter(self):
        self.client.post("/counters/foo")
        response = self.client.get("/counters/foo")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.get_json(), {"name": "foo", "counter": 0})

    def test_read_missing_counter(self):
        response = self.client.get("/counters/missing")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_counter(self):
        self.client.post("/counters/foo")
        response = self.client.put("/counters/foo")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.get_json(), {"name": "foo", "counter": 1})

    def test_update_missing_counter(self):
        response = self.client.put("/counters/missing")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_counter(self):
        self.client.post("/counters/foo")
        self.assertEqual(self.client.delete("/counters/foo").status_code, 204)
        self.assertEqual(self.client.delete("/counters/foo").status_code, 204)
        self.assertEqual(
            self.client.get("/counters/foo").status_code,
            status.HTTP_404_NOT_FOUND,
        )