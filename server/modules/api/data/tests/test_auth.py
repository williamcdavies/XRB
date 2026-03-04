from datetime                            import timedelta
from django_otp.plugins.otp_email.models import EmailDevice
from django.contrib.auth                 import get_user_model
from django.test                         import TestCase
from rest_framework_simplejwt.tokens     import RefreshToken
from rest_framework.test                 import APIClient
from unittest.mock                       import patch


User = get_user_model()


class AuthLoginTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.login_url = '/api/auth/login/'
        self.test_email = 'test@example.com'


    @patch.object(EmailDevice, 'generate_challenge')
    def test_login_creates_new_user(self, mock_generate):
        """Test that login creates a new user if email doesn't exist"""
        response = self.client.post(
            self.login_url,
            {
                'email': self.test_email,
                'role': 'default'
            },
            format='json'
        )
        
        self.assertEqual(response.status_code, 200)
        self.assertTrue(User.objects.filter(email=self.test_email).exists())
        mock_generate.assert_called_once()


    @patch.object(EmailDevice, 'generate_challenge')
    def test_login_existing_user(self, mock_generate):
        """Test that login works for existing user"""
        User.objects.create(email=self.test_email)
        
        response = self.client.post(
            self.login_url,
            {
                'email': self.test_email,
                'role': 'default'
            },
            format='json'
        )
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.filter(email=self.test_email).count(), 1)
        mock_generate.assert_called_once()


    @patch.object(EmailDevice, 'generate_challenge')
    def test_login_creates_email_device(self, mock_generate):
        """Test that login creates EmailDevice for user"""
        response = self.client.post(
            self.login_url,
            {
                'email': self.test_email,
                'role': 'default'
            },
            format='json'
        )
        
        self.assertEqual(response.status_code, 200)
        
        user = User.objects.get(email=self.test_email)
        self.assertTrue(
            EmailDevice.objects.filter(user=user, name='default').exists()
        )


    def test_login_invalid_email(self):
        """Test that invalid email returns 400"""
        response = self.client.post(
            self.login_url,
            {
                'email': 'not-an-email',
                'role': 'default'
            },
            format='json'
        )
        
        self.assertEqual(response.status_code, 400)


    def test_login_missing_email(self):
        """Test that missing email returns 400"""
        response = self.client.post(
            self.login_url,
            {'role': 'default'},
            format='json'
        )
        
        self.assertEqual(response.status_code, 400)


    def test_login_missing_role(self):
        """Test that missing role returns 400"""
        response = self.client.post(
            self.login_url,
            {'email': self.test_email},
            format='json'
        )
        
        self.assertEqual(response.status_code, 400)

    
    def test_login_invalid_role(self):
        """Test that invalid role returns 400"""
        response = self.client.post(
            self.login_url,
            {
                'email': self.test_email,
                'role': 'invalid_role'
            },
            format='json'
        )
        
        self.assertEqual(response.status_code, 400)

    @patch.object(EmailDevice, 'generate_challenge')
    def test_login_normalizes_email(self, mock_generate):
        """Test that email is normalized (lowercased, stripped)"""
        response = self.client.post(
            self.login_url,
            {
                'email': '  Test@Example.COM  ',
                'role': 'default'
            },
            format='json'
        )
        
        self.assertEqual(response.status_code, 200)
        self.assertTrue(User.objects.filter(email='test@example.com').exists())


class AuthVerifyTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.verify_url = '/api/auth/verify/'
        self.test_email = 'test@example.com'
        
        # Create user and email device
        self.user = User.objects.create(email=self.test_email)
        self.email_device = EmailDevice.objects.create(
            user=self.user,
            name='default',
            email=self.test_email,
            confirmed=True
        )


    @patch.object(EmailDevice, 'verify_token')
    def test_verify_valid_token(self, mock_verify):
        """Test successful verification with valid token"""
        mock_verify.return_value = True
        
        response = self.client.post(
            self.verify_url,
            {'email': self.test_email, 'token': '123456'},
            format='json'
        )
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('access', response.data)
        self.assertIn('refresh_token', response.cookies)


    @patch.object(EmailDevice, 'verify_token')
    def test_verify_invalid_token(self, mock_verify):
        """Test verification with invalid token returns 401"""
        mock_verify.return_value = False
        
        response = self.client.post(
            self.verify_url,
            {'email': self.test_email, 'token': '000000'},
            format='json'
        )
        
        self.assertEqual(response.status_code, 401)


    def test_verify_nonexistent_user(self):
        """Test verification with non-existent user returns 401"""
        response = self.client.post(
            self.verify_url,
            {'email': 'nonexistent@example.com', 'token': '123456'},
            format='json'
        )
        
        self.assertEqual(response.status_code, 401)


    def test_verify_missing_email(self):
        """Test verification without email returns 400"""
        response = self.client.post(
            self.verify_url,
            {'token': '123456'},
            format='json'
        )
        
        self.assertEqual(response.status_code, 400)


    def test_verify_missing_token(self):
        """Test verification without token returns 400"""
        response = self.client.post(
            self.verify_url,
            {'email': self.test_email},
            format='json'
        )
        
        self.assertEqual(response.status_code, 400)


    @patch.object(EmailDevice, 'verify_token')
    def test_verify_sets_httponly_cookie(self, mock_verify):
        """Test that refresh token is set as httponly cookie"""
        mock_verify.return_value = True
        
        response = self.client.post(
            self.verify_url,
            {'email': self.test_email, 'token': '123456'},
            format='json'
        )
        
        cookie = response.cookies.get('refresh_token')
        self.assertIsNotNone(cookie)
        self.assertTrue(cookie['httponly'])
        self.assertEqual(cookie['path'], '/')
        self.assertEqual(cookie['samesite'], 'Lax')


    @patch.object(EmailDevice, 'verify_token')
    def test_verify_returns_access_token(self, mock_verify):
        """Test that access token is returned in response body"""
        mock_verify.return_value = True
        
        response = self.client.post(
            self.verify_url,
            {'email': self.test_email, 'token': '123456'},
            format='json'
        )
        
        self.assertIn('access', response.data)
        self.assertTrue(len(response.data['access']) > 0)


class AuthRefreshTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.refresh_url = '/api/auth/refresh/'
        self.test_email = 'test@example.com'
        
        # Create user
        self.user = User.objects.create(email=self.test_email)
        
        # Generate refresh token
        self.refresh_token = RefreshToken.for_user(self.user)


    def test_refresh_with_valid_token(self):
        """Test refresh with valid refresh token"""
        self.client.cookies['refresh_token'] = str(self.refresh_token)
        
        response = self.client.post(self.refresh_url)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('access', response.data)
        self.assertIn('refresh_token', response.cookies)


    def test_refresh_without_cookie(self):
        """Test refresh without refresh token cookie returns 401"""
        response = self.client.post(self.refresh_url)
        
        self.assertEqual(response.status_code, 401)


    def test_refresh_with_invalid_token(self):
        """Test refresh with invalid token returns 401"""
        self.client.cookies['refresh_token'] = 'invalid-token'
        
        response = self.client.post(self.refresh_url)
        
        self.assertEqual(response.status_code, 401)


    def test_refresh_with_expired_token(self):
        """Test refresh with expired token returns 401"""
        # Create an expired token
        expired_token = RefreshToken.for_user(self.user)
        expired_token.set_exp(lifetime=timedelta(seconds=-1))
        
        self.client.cookies['refresh_token'] = str(expired_token)
        
        response = self.client.post(self.refresh_url)
        
        self.assertEqual(response.status_code, 401)


    def test_refresh_blacklists_old_token(self):
        """Test that old refresh token is blacklisted after refresh"""
        old_token = str(self.refresh_token)
        self.client.cookies['refresh_token'] = old_token
        
        # First refresh should succeed
        response = self.client.post(self.refresh_url)
        self.assertEqual(response.status_code, 200)
        
        # Second refresh with same token should fail (blacklisted)
        self.client.cookies['refresh_token'] = old_token
        response = self.client.post(self.refresh_url)
        self.assertEqual(response.status_code, 401)


    def test_refresh_returns_new_tokens(self):
        """Test that new access and refresh tokens are returned"""
        old_token = str(self.refresh_token)
        self.client.cookies['refresh_token'] = old_token
        
        response = self.client.post(self.refresh_url)
        
        # New access token in response
        self.assertIn('access', response.data)
        
        # New refresh token in cookie
        new_cookie_token = response.cookies.get('refresh_token').value
        self.assertNotEqual(old_token, new_cookie_token)


    def test_refresh_with_deleted_user(self):
        """Test refresh fails if user was deleted"""
        self.client.cookies['refresh_token'] = str(self.refresh_token)
        
        self.user.delete()
        
        response = self.client.post(self.refresh_url)
        
        self.assertEqual(response.status_code, 401)


    def test_refresh_cookie_attributes(self):
        """Test that new refresh token cookie has correct attributes"""
        self.client.cookies['refresh_token'] = str(self.refresh_token)
        
        response = self.client.post(self.refresh_url)
        
        cookie = response.cookies.get('refresh_token')
        self.assertTrue(cookie['httponly'])
        self.assertEqual(cookie['path'], '/')
        self.assertEqual(cookie['samesite'], 'Lax')
        self.assertIsNotNone(cookie['max-age'])


class AuthIntegrationTests(TestCase):
    """Integration tests for the full auth flow"""
    

    def setUp(self):
        self.client = APIClient()
        self.test_email = 'integration@example.com'


    @patch.object(EmailDevice, 'generate_challenge')
    @patch.object(EmailDevice, 'verify_token')
    def test_full_auth_flow(self, mock_verify, mock_generate):
        """Test complete flow: login -> verify -> refresh"""
        mock_verify.return_value = True
        
        # Step 1: Login
        login_response = self.client.post(
            '/api/auth/login/',
            {
                'email': self.test_email,
                'role': 'default'
            },
            format='json'
        )
        self.assertEqual(login_response.status_code, 200)
        
        # Step 2: Verify
        verify_response = self.client.post(
            '/api/auth/verify/',
            {'email': self.test_email, 'token': '123456'},
            format='json'
        )
        self.assertEqual(verify_response.status_code, 200)
        access_token = verify_response.data['access']
        
        # Step 3: Refresh
        refresh_response = self.client.post('/api/auth/refresh/')
        self.assertEqual(refresh_response.status_code, 200)
        new_access_token = refresh_response.data['access']
        
        self.assertNotEqual(access_token, new_access_token)