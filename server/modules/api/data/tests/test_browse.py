from modules.api.data.tests.test_base import DataEndpointTestBase

class BrowseEndpointTests(DataEndpointTestBase):

    def test_unauthenticated_browse(self):
        response = self.unauthenticated_client.get("/api/data/browse/")

        # access base directory - expect 200
        self.assertEqual(response.status_code, 200)

        # access public folder - expect 200
        response = self.unauthenticated_client.get("/api/data/browse/", {"path": "public"})
        self.assertIn("items", response.data)

        # try to access users/ root - expect 403
        response = self.unauthenticated_client.get("/api/data/browse/", {"path": "users"})
        self.assertEqual(response.status_code, 403)

        # try to access some user - expect 403
        response = self.unauthenticated_client.get("/api/data/browse/", {"path": "users/abc"})
        self.assertEqual(response.status_code, 403)

        # try to access some group - expect 403
        response = self.unauthenticated_client.get("/api/data/browse/", {"path": "groups/abc"})
        self.assertEqual(response.status_code, 403)

    def test_authenticated_browse(self):
        response = self.authenticated_client.get("/api/data/browse/")

        # access base directory - expect 200 with public, user dir, and group dir
        self.assertEqual(response.status_code, 200)
        self.assertIn({"name": "public", "path": "public", "type": "directory"}, response.data["items"])
        self.assertIn({"name": "test@example.com", "path": "users/test@example.com", "type": "directory"}, response.data["items"])
        self.assertIn({"name": "astro-lab", "path": "groups/astro-lab", "type": "directory"}, response.data["items"])

        # access public folder - expect 200
        response = self.authenticated_client.get("/api/data/browse/", {"path": "public"})
        self.assertIn("items", response.data)

        # access users/ root - expect 200 with only own directory listed
        response = self.authenticated_client.get("/api/data/browse/", {"path": "users"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["items"]), 1)
        self.assertEqual(response.data["items"][0]["path"], "users/test@example.com")

        # access own user directory - expect 200
        response = self.authenticated_client.get("/api/data/browse/", {"path": "users/test@example.com"})
        self.assertEqual(response.status_code, 200)

        # access own group directory - expect 200
        response = self.authenticated_client.get("/api/data/browse/", {"path": "groups/astro-lab"})
        self.assertEqual(response.status_code, 200)

        # access another user's directory - expect 403
        response = self.authenticated_client.get("/api/data/browse/", {"path": "users/other@example.com"})
        self.assertEqual(response.status_code, 403)

        # access a group the user doesn't belong to - expect 403
        response = self.authenticated_client.get("/api/data/browse/", {"path": "groups/secret-group"})
        self.assertEqual(response.status_code, 403)

    def test_browse_users_root_when_dir_missing(self):
        import shutil
        shutil.rmtree(self.tmp / "users" / "test@example.com")

        response = self.authenticated_client.get("/api/data/browse/", {"path": "users"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["items"], [])