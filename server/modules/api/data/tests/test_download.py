from modules.api.data.tests.test_base import DataEndpointTestBase


class DownloadEndpointTests(DataEndpointTestBase):

    def _create_file(self, relative_path, content=b"file content"):
        path = self.tmp / relative_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(content)
        return path

    def test_download_from_public(self):
        self._create_file("public/readme.txt")
        response = self.unauthenticated_client.get(
            "/api/data/download/", {"path": "public/readme.txt"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(b"".join(response.streaming_content), b"file content")

    def test_download_from_own_user_dir(self):
        self._create_file("users/test@example.com/data.csv")
        response = self.authenticated_client.get(
            "/api/data/download/", {"path": "users/test@example.com/data.csv"}
        )
        self.assertEqual(response.status_code, 200)

    def test_download_from_own_group_dir(self):
        self._create_file("groups/astro-lab/results.csv")
        response = self.authenticated_client.get(
            "/api/data/download/", {"path": "groups/astro-lab/results.csv"}
        )
        self.assertEqual(response.status_code, 200)

    def test_download_from_other_user_dir_denied(self):
        self._create_file("users/otheruser/secret.txt")
        response = self.authenticated_client.get(
            "/api/data/download/", {"path": "users/otheruser/secret.txt"}
        )
        self.assertEqual(response.status_code, 403)

    def test_download_from_other_group_denied(self):
        self._create_file("groups/secret-group/data.txt")
        response = self.authenticated_client.get(
            "/api/data/download/", {"path": "groups/secret-group/data.txt"}
        )
        self.assertEqual(response.status_code, 403)

    def test_download_user_dir_unauthenticated_denied(self):
        self._create_file("users/test@example.com/file.txt")
        response = self.unauthenticated_client.get(
            "/api/data/download/", {"path": "users/test@example.com/file.txt"}
        )
        self.assertEqual(response.status_code, 403)

    def test_download_missing_path_param(self):
        response = self.authenticated_client.get("/api/data/download/")
        self.assertEqual(response.status_code, 400)

    def test_download_nonexistent_file(self):
        response = self.authenticated_client.get(
            "/api/data/download/", {"path": "public/nope.txt"}
        )
        self.assertEqual(response.status_code, 404)

    def test_download_directory_returns_400(self):
        response = self.authenticated_client.get(
            "/api/data/download/", {"path": "public"}
        )
        self.assertEqual(response.status_code, 400)