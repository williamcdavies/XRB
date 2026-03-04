from modules.api.data.tests.test_base import DataEndpointTestBase
from django.core.files.uploadedfile import SimpleUploadedFile

class UploadEndpointTests(DataEndpointTestBase):

    def _make_file(self, name="test.txt", content=b"hello world"):
        return SimpleUploadedFile(name, content, content_type="text/plain")

    def test_upload_to_own_user_dir(self):
        response = self.authenticated_client.post(
            "/api/data/upload/",
            {"file": self._make_file(), "path": "users/test@example.com"},
            format="multipart",
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["name"], "test.txt")
        self.assertTrue((self.tmp / "users" / "test@example.com" / "test.txt").exists())

    def test_upload_to_own_group_dir(self):
        response = self.authenticated_client.post(
            "/api/data/upload/",
            {"file": self._make_file(), "path": "groups/astro-lab"},
            format="multipart",
        )
        self.assertEqual(response.status_code, 201)
        self.assertTrue((self.tmp / "groups" / "astro-lab" / "test.txt").exists())

    def test_upload_to_public(self):
        response = self.authenticated_client.post(
            "/api/data/upload/",
            {"file": self._make_file(), "path": "public"},
            format="multipart",
        )
        self.assertEqual(response.status_code, 201)

    def test_upload_to_other_user_dir_denied(self):
        (self.tmp / "users" / "otheruser").mkdir(parents=True, exist_ok=True)
        response = self.authenticated_client.post(
            "/api/data/upload/",
            {"file": self._make_file(), "path": "users/otheruser"},
            format="multipart",
        )
        self.assertEqual(response.status_code, 403)

    def test_upload_to_other_group_denied(self):
        response = self.authenticated_client.post(
            "/api/data/upload/",
            {"file": self._make_file(), "path": "groups/secret-group"},
            format="multipart",
        )
        self.assertEqual(response.status_code, 403)

    def test_upload_missing_file(self):
        response = self.authenticated_client.post(
            "/api/data/upload/",
            {"path": "public"},
            format="multipart",
        )
        self.assertEqual(response.status_code, 400)

    def test_upload_missing_path(self):
        response = self.authenticated_client.post(
            "/api/data/upload/",
            {"file": self._make_file()},
            format="multipart",
        )
        self.assertEqual(response.status_code, 400)

    def test_upload_unauthenticated(self):
        response = self.unauthenticated_client.post(
            "/api/data/upload/",
            {"file": self._make_file(), "path": "public"},
            format="multipart",
        )
        self.assertEqual(response.status_code, 401)

    def test_upload_sanitizes_filename(self):
        f = self._make_file(name="my file.txt")
        response = self.authenticated_client.post(
            "/api/data/upload/",
            {"file": f, "path": "users/test@example.com"},
            format="multipart",
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["name"], "my_file.txt")

    def test_upload_response_fields(self):
        response = self.authenticated_client.post(
            "/api/data/upload/",
            {"file": self._make_file(content=b"12345"), "path": "users/test@example.com"},
            format="multipart",
        )
        self.assertEqual(response.status_code, 201)
        self.assertIn("path", response.data)
        self.assertIn("name", response.data)
        self.assertIn("size", response.data)
        self.assertEqual(response.data["size"], 5)
        self.assertIn("type", response.data)
        self.assertEqual(response.data["type"], "txt")