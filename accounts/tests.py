from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import SESSION_KEY


from .models import User


class TestSignUpView(TestCase):
    def test_success_get(self):
        res = self.client.get(reverse('accounts:signup'))
        self.assertEqual(res.status_code, 200)

    def test_success_post(self):
        data = {
                "username": "test",
                "email": "test@example.com",
                "password1": "examplepassword",
                "password2": "examplepassword",
                }
        res = self.client.post(reverse('accounts:signup'), data)
        self.assertRedirects(
                res,
                reverse('tweets:home'),
                status_code=302,
                target_status_code=200,
                )
        self.assertEqual(User.objects.all().count(), 1)
        self.assertEqual(
                User.objects.filter(
                    username='test', email='test@example.com'
                    ).count(),
                1,
                )
        self.assertIn(SESSION_KEY, self.client.session)

    def test_failure_post_with_empty_form(self):
        data = {
                'username': '',
                'email': '',
                'password1': '',
                'password2': '',
                }
        response = self.client.post(reverse('accounts:signup'), data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.all().count(), 0)
        self.assertFormError(response, "form", "username", ["このフィールドは必須です。"])
        self.assertFormError(response, "form", "email", ["このフィールドは必須です。"])
        self.assertFormError(response, "form", "password1", ["このフィールドは必須です。"])
        self.assertFormError(response, "form", "password2", ["このフィールドは必須です。"])

    def test_failure_post_with_empty_username(self):
        data = {
                'username': '',
                'email': 'test@example.com',
                'password1': 'abcd1234',
                'password2': 'abcd1234',
                }
        response = self.client.post(reverse('accounts:signup'), data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.all().count(), 0)
        self.assertFormError(response, "form", "username", ["このフィールドは必須です。"])

    def test_failure_post_with_empty_email(self):
        data = {
                'username': 'test',
                'email': '',
                'password1': 'abcd1234',
                'password2': 'abcd1234',
                }
        response = self.client.post(reverse('accounts:signup'), data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.all(). count(), 0)
        self.assertFormError(response, "form", "email", ['このフィールドは必須です。'])

    def test_failure_post_with_empty_password(self):
        data = {
                'username': 'test',
                'email': 'test@example.com',
                'password1': '',
                'password2': '',
                }
        response = self.client.post(reverse('accounts:signup'), data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.all(). count(), 0)
        self.assertFormError(response, "form", "password1", "このフィールドは必須です。")
        self.assertFormError(response, "form", "password2", "このフィールドは必須です。")

    def test_failure_post_with_duplicated_user(self):
        User.objects.create_user(
                username='test',
                email='test@example.com',
                password='abcd1234',
                )
        data = {
                'username': 'test',
                'email': 'test@example.com',
                'password1': 'abcd1234',
                'password2': 'abcd1234',
                }
        response = self.client.post(reverse('accounts:signup'), data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.all().count(), 1)

    def test_failure_post_with_invalid_email(self):
        data = {
                'username': 'test',
                'email': 'test',
                'password1': 'abcd1234',
                'password2': 'abcd1234',
                }
        response = self.client.post(reverse('accounts:signup'), data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.all().count(), 0)

    def test_failure_post_with_too_short_password(self):
        data = {
                'username': 'test',
                'email': 'test@example.com',
                'password1': 'abcd',
                'password2': 'abcd',
                }
        response = self.client.post(reverse('accounts:signup'), data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.all().count(), 0)

    def test_failure_post_with_password_similar_to_username(self):
        data = {
                'username': 'test',
                'email': 'test@example.com',
                'password1': 'test',
                'password2': 'test',
                }
        response = self.client.post(reverse('accounts:signup'), data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.all().count(), 0)

    def test_failure_post_with_only_numbers_password(self):
        data = {
                'username': 'test',
                'email': 'test@example.com',
                'password1': '271828',
                'password2': '271828',
                }
        response = self.client.post(reverse('accounts:signup'), data=data)
        self.assertEqual(response.status_code, 200)
 #       self.assertEqual(response.objects.all().count(), 0)

    def test_failure_post_with_mismatch_password(self):
        data = {
                'username': 'test',
                'email': 'test@example.com',
                'password1': 'abcd1234',
                'password2': '1234abcd',
                }
        response = self.client.post(reverse('accounts:signup'), data=data)
        self.assertEqual(response.status_code, 200)
#        self.assertEqual(response.objects.all().count(), 0)


class TestLoginView(TestCase):
    def test_success_get(self):
        pass

    def test_success_post(self):
        pass

    def test_failure_post_with_not_exists_user(self):
        pass

    def test_failure_post_with_empty_password(self):
        pass


class TestLogoutView(TestCase):
    def test_success_get(self):
        pass


class TestUserProfileView(TestCase):
    def test_success_get(self):
        pass


class TestUserProfileEditView(TestCase):
    def test_success_get(self):
        pass

    def test_success_post(self):
        pass

    def test_failure_post_with_not_exists_user(self):
        pass

    def test_failure_post_with_incorrect_user(self):
        pass


class TestFollowView(TestCase):
    def test_success_post(self):
        pass

    def test_failure_post_with_not_exist_user(self):
        pass

    def test_failure_post_with_self(self):
        pass


class TestUnfollowView(TestCase):
    def test_success_post(self):
        pass

    def test_failure_post_with_not_exist_tweet(self):
        pass

    def test_failure_post_with_incorrect_user(self):
        pass


class TestFollowingListView(TestCase):
    def test_success_get(self):
        pass


class TestFollowerListView(TestCase):
    def test_success_get(self):
        pass
