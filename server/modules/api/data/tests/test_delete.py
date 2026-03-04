from modules.api.data.tests.test_base import DataEndpointTestBase


class DeleteEndpointTests(DataEndpointTestBase):

    def _create_file(self, relative_path, content=b"data"):
        path = self.tmp / relative_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(content)
        return path

    def test_delete_own_file(self):
        self._create_file("users/test@example.com/old.txt")
        response = self.authenticated_client.delete(
            "/api/data/delete/?path=users/test@example.com/old.txt"
        )
        self.assertEqual(response.status_code, 204)
        self.assertFalse((self.tmp / "users" / "test@example.com" / "old.txt").exists())

    def test_delete_own_directory(self):
        subdir = self.tmp / "users" / "test@example.com" / "subdir"
        subdir.mkdir()
        (subdir / "file.txt").write_bytes(b"x")
        response = self.authenticated_client.delete(
            "/api/data/delete/?path=users/test@example.com/subdir"
        )
        self.assertEqual(response.status_code, 204)
        self.assertFalse(subdir.exists())

    def test_delete_in_group_dir(self):
        self._create_file("groups/astro-lab/old.csv")
        response = self.authenticated_client.delete(
            "/api/data/delete/?path=groups/astro-lab/old.csv"
        )
        self.assertEqual(response.status_code, 204)

    def test_delete_in_public(self):
        self._create_file("public/junk.txt")
        response = self.authenticated_client.delete(
            "/api/data/delete/?path=public/junk.txt"
        )
        self.assertEqual(response.status_code, 204)

    def test_delete_other_user_dir_denied(self):
        self._create_file("users/otheruser/private.txt")
        response = self.authenticated_client.delete(
            "/api/data/delete/?path=users/otheruser/private.txt"
        )
        self.assertEqual(response.status_code, 403)

    def test_delete_other_group_denied(self):
        self._create_file("groups/secret-group/data.txt")
        response = self.authenticated_client.delete(
            "/api/data/delete/?path=groups/secret-group/data.txt"
        )
        self.assertEqual(response.status_code, 403)

    def test_delete_missing_path(self):
        response = self.authenticated_client.delete("/api/data/delete/")
        self.assertEqual(response.status_code, 400)

    def test_delete_nonexistent(self):
        response = self.authenticated_client.delete(
            "/api/data/delete/?path=public/ghost.txt"
        )
        self.assertEqual(response.status_code, 404)

    def test_delete_unauthenticated(self):
        self._create_file("public/target.txt")
        response = self.unauthenticated_client.delete(
            "/api/data/delete/?path=public/target.txt"
        )
        self.assertEqual(response.status_code, 401)
