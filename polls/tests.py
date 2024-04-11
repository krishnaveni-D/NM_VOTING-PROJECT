from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone

from .models import Poll, Vote


class PollModelTest(TestCase):
    def test_user_can_vote(self):
        user = User.objects.create_user('krish')
        poll = Poll.objects.create(owner=user)
        self.assertTrue(poll.user_can_vote(user))

        choice = poll.choice_set.create(choice_text='pizza')
        Vote.objects.create(user=user, poll=poll, choice=choice)
        self.assertFalse(poll.user_can_vote(user))


class PollViewTest(TestCase):
    def test_home(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_login(self):
        User.objects.create_user(username='krish', password='voted')
        response = self.client.post(
            '/accounts/login/', {'username': 'krish', 'password': 'voted'}
        )
        self.assertRedirects(response, '/')

    def test_register(self):
        response = self.client.post(
            '/accounts/register/',
            {
                'username': 'krish',
                'password1': 'voted',
                'password2': 'voted',
                'email': 'krish123@gmail.com',
            },
        )
        self.assertRedirects(response, '/accounts/login/')
        # assert that user got actually created in the backend
        self.assertIsNotNone(authenticate(username='krish', password='voted'))
