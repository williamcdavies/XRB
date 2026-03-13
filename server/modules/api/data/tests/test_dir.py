from modules.api.data.tests.test_base import DataEndpointTestBase


class MkdirEndpointTests(DataEndpointTestBase):

    def test_mkdir_in_own_user_dir(self):
        response = self.authenticated_client.post(
            "/api/data/mkdir/",
            {"path": "users/test@example.com", "name": "results"},
            format="json",
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["name"], "results")
        self.assertTrue((self.tmp / "users" / "test@example.com" / "results").is_dir())

    def test_mkdir_in_own_group_dir(self):
        response = self.authenticated_client.post(
            "/api/data/mkdir/",
            {"path": "groups/astro-lab", "name": "datasets"},
            format="json",
        )
        self.assertEqual(response.status_code, 201)

    def test_mkdir_in_public(self):
        response = self.authenticated_client.post(
            "/api/data/mkdir/",
            {"path": "public", "name": "shared"},
            format="json",
        )
        self.assertEqual(response.status_code, 201)

    def test_mkdir_in_other_user_dir_denied(self):
        (self.tmp / "users" / "otheruser").mkdir(parents=True, exist_ok=True)
        response = self.authenticated_client.post(
            "/api/data/mkdir/",
            {"path": "users/otheruser", "name": "hack"},
            format="json",
        )
        self.assertEqual(response.status_code, 403)

    def test_mkdir_in_other_group_denied(self):
        response = self.authenticated_client.post(
            "/api/data/mkdir/",
            {"path": "groups/secret-group", "name": "nope"},
            format="json",
        )
        self.assertEqual(response.status_code, 403)

    def test_mkdir_missing_path(self):
        response = self.authenticated_client.post(
            "/api/data/mkdir/",
            {"name": "orphan"},
            format="json",
        )
        self.assertEqual(response.status_code, 400)

    def test_mkdir_missing_name(self):
        response = self.authenticated_client.post(
            "/api/data/mkdir/",
            {"path": "public"},
            format="json",
        )
        self.assertEqual(response.status_code, 400)

    def test_mkdir_name_with_slashes(self):
        response = self.authenticated_client.post(
            "/api/data/mkdir/",
            {"path": "public", "name": "bad/name"},
            format="json",
        )
        self.assertEqual(response.status_code, 400)

    def test_mkdir_duplicate_returns_409(self):
        (self.tmp / "public" / "existing").mkdir()
        response = self.authenticated_client.post(
            "/api/data/mkdir/",
            {"path": "public", "name": "existing"},
            format="json",
        )
        self.assertEqual(response.status_code, 409)

    def test_mkdir_sanitizes_spaces(self):
        response = self.authenticated_client.post(
            "/api/data/mkdir/",
            {"path": "users/test@example.com", "name": "my folder"},
            format="json",
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["name"], "my folder")

    def test_mkdir_creates_personal_dir(self):
        import shutil
        shutil.rmtree(self.tmp / "users" / "test@example.com")

        response = self.authenticated_client.post(
            "/api/data/mkdir/",
            {"path": "users", "name": "test@example.com"},
            format="json",
        )
        self.assertEqual(response.status_code, 201)
        self.assertTrue((self.tmp / "users" / "test@example.com").is_dir())

    def test_mkdir_unauthenticated(self):
        response = self.unauthenticated_client.post(
            "/api/data/mkdir/",
            {"path": "public", "name": "anon"},
            format="json",
        )
        self.assertEqual(response.status_code, 401  )