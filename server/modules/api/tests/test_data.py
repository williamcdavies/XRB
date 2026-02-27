import shutil
import tempfile
from pathlib import Path
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APITestCase, APIClient

User = get_user_model()


class DataEndpointTestBase(APITestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.patcher = patch('modules.api.data.views.BASE_DATA_DIR', self.tmp)
        self.patcher.start()

        (self.tmp / 'public').mkdir()
        (self.tmp / 'users' / 'testuser').mkdir(parents=True)
        (self.tmp / 'groups' / 'astro-lab').mkdir(parents=True)

        self.user = User.objects.create_user(username='testuser', email='test@example.com')
        self.group = Group.objects.create(name='astro-lab')
        self.user.groups.add(self.group)

        self.authenticated_client = APIClient()
        self.authenticated_client.force_authenticate(user=self.user)

        self.unauthenticated_client = APIClient()

    def tearDown(self):
        self.patcher.stop()
        shutil.rmtree(self.tmp, ignore_errors=True)

class BrowseEndpointTests(DataEndpointTestBase):

    def test_unauthenticated_browse(self):
        response = self.unauthenticated_client.get("/api/data/browse/")

        # access base directory - expect 200
        self.assertEqual(response.status_code, 200)
        

        # access public folder - expect 200
        response = self.unauthenticated_client.get("/api/data/browse/", {"path": "public"})
        self.assertIn("items", response.data)
        

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
        self.assertIn({"name": "testuser", "path": "users/testuser", "type": "directory"}, response.data["items"])
        self.assertIn({"name": "astro-lab", "path": "groups/astro-lab", "type": "directory"}, response.data["items"])
        

        # access public folder - expect 200
        response = self.authenticated_client.get("/api/data/browse/", {"path": "public"})
        self.assertIn("items", response.data)
        

        # access own user directory - expect 200
        response = self.authenticated_client.get("/api/data/browse/", {"path": "users/testuser"})
        self.assertEqual(response.status_code, 200)
        

        # access own group directory - expect 200
        response = self.authenticated_client.get("/api/data/browse/", {"path": "groups/astro-lab"})
        self.assertEqual(response.status_code, 200)
        

        # access another user's directory - expect 403
        response = self.authenticated_client.get("/api/data/browse/", {"path": "users/otheruser"})
        self.assertEqual(response.status_code, 403)
        

        # access a group the user doesn't belong to - expect 403
        response = self.authenticated_client.get("/api/data/browse/", {"path": "groups/secret-group"})
        self.assertEqual(response.status_code, 403)
        


class UploadEndpointTests(DataEndpointTestBase):

    def _make_file(self, name="test.txt", content=b"hello world"):
        return SimpleUploadedFile(name, content, content_type="text/plain")

    def test_upload_to_own_user_dir(self):
        response = self.authenticated_client.post(
            "/api/data/upload/",
            {"file": self._make_file(), "path": "users/testuser"},
            format="multipart",
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["name"], "test.txt")
        self.assertTrue((self.tmp / "users" / "testuser" / "test.txt").exists())

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
            {"file": f, "path": "users/testuser"},
            format="multipart",
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["name"], "my_file.txt")

    def test_upload_response_fields(self):
        response = self.authenticated_client.post(
            "/api/data/upload/",
            {"file": self._make_file(content=b"12345"), "path": "users/testuser"},
            format="multipart",
        )
        self.assertEqual(response.status_code, 201)
        self.assertIn("path", response.data)
        self.assertIn("name", response.data)
        self.assertIn("size", response.data)
        self.assertEqual(response.data["size"], 5)
        self.assertIn("type", response.data)
        self.assertEqual(response.data["type"], "txt")


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
        self._create_file("users/testuser/data.csv")
        response = self.authenticated_client.get(
            "/api/data/download/", {"path": "users/testuser/data.csv"}
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
        self._create_file("users/testuser/file.txt")
        response = self.unauthenticated_client.get(
            "/api/data/download/", {"path": "users/testuser/file.txt"}
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


class MkdirEndpointTests(DataEndpointTestBase):

    def test_mkdir_in_own_user_dir(self):
        response = self.authenticated_client.post(
            "/api/data/mkdir/",
            {"path": "users/testuser", "name": "results"},
            format="json",
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["name"], "results")
        self.assertTrue((self.tmp / "users" / "testuser" / "results").is_dir())

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
            {"path": "users/testuser", "name": "my folder"},
            format="json",
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["name"], "my_folder")

    def test_mkdir_unauthenticated(self):
        response = self.unauthenticated_client.post(
            "/api/data/mkdir/",
            {"path": "public", "name": "anon"},
            format="json",
        )
        self.assertEqual(response.status_code, 401  )


class DeleteEndpointTests(DataEndpointTestBase):

    def _create_file(self, relative_path, content=b"data"):
        path = self.tmp / relative_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(content)
        return path

    def test_delete_own_file(self):
        self._create_file("users/testuser/old.txt")
        response = self.authenticated_client.delete(
            "/api/data/delete/?path=users/testuser/old.txt"
        )
        self.assertEqual(response.status_code, 204)
        self.assertFalse((self.tmp / "users" / "testuser" / "old.txt").exists())

    def test_delete_own_directory(self):
        subdir = self.tmp / "users" / "testuser" / "subdir"
        subdir.mkdir()
        (subdir / "file.txt").write_bytes(b"x")
        response = self.authenticated_client.delete(
            "/api/data/delete/?path=users/testuser/subdir"
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
