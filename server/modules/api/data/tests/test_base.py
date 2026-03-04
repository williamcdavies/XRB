import shutil
import tempfile
from pathlib import Path
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from rest_framework.test import APITestCase, APIClient

User = get_user_model()

class DataEndpointTestBase(APITestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.patcher = patch('modules.api.data.views.BASE_DATA_DIR', self.tmp)
        self.patcher.start()

        (self.tmp / 'public').mkdir()
        (self.tmp / 'users' / 'test@example.com').mkdir(parents=True)
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