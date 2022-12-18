from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import SESSION_KEY


from django.contrib.auth import get_user_model
User = get_user_model()


class TestSignUpView(TestCase):
    def test_success_get(self):
        res = self.client.get(reverse("accounts:signup"))
        self.assertEqual(res.status_code, 200)

    def test_success_post(self):
        data = {
            "username": "test",
            "email": "test@example.com",
            "password1": "examplepassword",
            "password2": "examplepassword",
        }
        res = self.client.post(reverse("accounts:signup"), data)
        self.assertRedirects(
            res,
            reverse("tweets:home"),
            status_code=302,
            target_status_code=200,
        )
        self.assertEqual(User.objects.all().count(), 1)
        self.assertEqual(
            User.objects.filter(username="test", email="test@example.com").count(),
            1,
        )
        self.assertIn(SESSION_KEY, self.client.session)

    def test_failure_post_with_empty_form(self):
        data = {
            "username": "",
            "email": "",
            "password1": "",
            "password2": "",
        }
        response = self.client.post(reverse("accounts:signup"), data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.all().count(), 0)
        form = response.context["form"]
        self.assertEqual(form.errors["username"], ["このフィールドは必須です。"])
        self.assertEqual(form.errors["email"], ["このフィールドは必須です。"])
        self.assertEqual(form.errors["password1"], ["このフィールドは必須です。"])
        self.assertEqual(form.errors["password2"], ["このフィールドは必須です。"])

    def test_failure_post_with_empty_username(self):
        data = {
            "username": "",
            "email": "test@example.com",
            "password1": "abcd1234",
            "password2": "abcd1234",
        }
        response = self.client.post(reverse("accounts:signup"), data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.all().count(), 0)
        form = response.context["form"]
        self.assertEqual(form.errors["username"], ["このフィールドは必須です。"])

    def test_failure_post_with_empty_email(self):
        data = {
            "username": "test",
            "email": "",
            "password1": "abcd1234",
            "password2": "abcd1234",
        }
        response = self.client.post(reverse("accounts:signup"), data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.all().count(), 0)
        form = response.context["form"]
        self.assertEqual(form.errors["email"], ["このフィールドは必須です。"])

    def test_failure_post_with_empty_password(self):
        data = {
            "username": "test",
            "email": "test@example.com",
            "password1": "",
            "password2": "",
        }
        response = self.client.post(reverse("accounts:signup"), data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.all().count(), 0)
        form = response.context["form"]
        self.assertEqual(form.errors["password1"], ["このフィールドは必須です。"])
        self.assertEqual(form.errors["password2"], ["このフィールドは必須です。"])

    def test_failure_post_with_duplicated_user(self):
        User.objects.create_user(
            username="test",
            email="test@example.com",
            password="abcd1234",
        )
        data = {
            "username": "test",
            "email": "test@example.com",
            "password1": "abcd1234",
            "password2": "abcd1234",
        }
        response = self.client.post(reverse("accounts:signup"), data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.all().count(), 1)
        form = response.context["form"]
        self.assertEqual(form.errors["username"], ["同じユーザー名が既に登録済みです。"])

    def test_failure_post_with_invalid_email(self):
        data = {
            "username": "test",
            "email": "test",
            "password1": "abcd1234",
            "password2": "abcd1234",
        }
        response = self.client.post(reverse("accounts:signup"), data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.all().count(), 0)
        form = response.context["form"]
        self.assertEqual(form.errors["email"], ["有効なメールアドレスを入力してください。"])

    def test_failure_post_with_too_short_password(self):
        data = {
            "username": "test",
            "email": "test@example.com",
            "password1": "sjci",
            "password2": "sjci",
        }
        response = self.client.post(reverse("accounts:signup"), data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.all().count(), 0)
        form = response.context["form"]
        self.assertEqual(form.errors["password2"], ["このパスワードは短すぎます。最低 8 文字以上必要です。"])

    def test_failure_post_with_password_similar_to_username(self):
        data = {
            "username": "cjigsefg",
            "email": "test@example.com",
            "password1": "cjigsefg",
            "password2": "cjigsefg",
        }
        response = self.client.post(reverse("accounts:signup"), data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.all().count(), 0)
        form = response.context["form"]
        self.assertEqual(form.errors["password2"], ["このパスワードは ユーザー名 と似すぎています。"])

    def test_failure_post_with_only_numbers_password(self):
        data = {
            "username": "test",
            "email": "test@example.com",
            "password1": "27182818",
            "password2": "27182818",
        }
        response = self.client.post(reverse("accounts:signup"), data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.all().count(), 0)
        form = response.context["form"]
        self.assertEqual(form.errors["password2"], ["このパスワードは数字しか使われていません。"])

    def test_failure_post_with_mismatch_password(self):
        data = {
            "username": "test",
            "email": "test@example.com",
            "password1": "abcd1234",
            "password2": "1234abcd",
        }
        response = self.client.post(reverse("accounts:signup"), data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.all().count(), 0)
        form = response.context["form"]
        self.assertEqual(form.errors["password2"], ["確認用パスワードが一致しません。"])


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
