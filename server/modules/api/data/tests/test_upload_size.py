from unittest.mock import patch

from django.core.files.uploadedfile import SimpleUploadedFile

from modules.api.data.tests.test_base import DataEndpointTestBase


class UploadSizeLimitTests(DataEndpointTestBase):

    def _make_file(self, name="test.txt", size=1024):
        return SimpleUploadedFile(name, b"x" * size, content_type="text/plain")

    def test_upload_under_limit_succeeds(self):
        response = self.authenticated_client.post(
            "/api/data/upload/",
            {"file": self._make_file(size=1024), "path": "public"},
            format="multipart",
        )
        self.assertEqual(response.status_code, 201)

    @patch("modules.api.data.views.MAX_UPLOAD_SIZE", 100)
    def test_upload_over_limit_returns_413(self):
        response = self.authenticated_client.post(
            "/api/data/upload/",
            {"file": self._make_file(size=200), "path": "public"},
            format="multipart",
        )
        self.assertEqual(response.status_code, 413)
        self.assertIn("5 GB", response.data["error"])

    @patch("modules.api.data.views.MAX_UPLOAD_SIZE", 100)
    def test_upload_exactly_at_limit_succeeds(self):
        response = self.authenticated_client.post(
            "/api/data/upload/",
            {"file": self._make_file(size=100), "path": "public"},
            format="multipart",
        )
        self.assertEqual(response.status_code, 201)
