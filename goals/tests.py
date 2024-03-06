from django.contrib.auth.models import User
from .models import Goal
from focus.models import Focus
from rest_framework import status
from rest_framework.test import APITestCase


class GoalListViewTests(APITestCase):
    """
    Tests for the Goal list view
    """
    def setUp(self):
        first_tester = User.objects.create_user(username='FirstTester', password='pass')
        Focus.objects.create(
            owner=first_tester, name="Name", why="Why"
        )

    def test_logged_out_no_create_goal(self):
        """
        Not logged in user sending HTTP post request, should return 403 error
        """
        response = self.client.post(
            '/goals/', {"title": "title", "focus": 1})
        count = Goal.objects.count()
        self.assertEqual(count, 0)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_logged_in_can_create_goal(self):
        """
        Logged in user sending a post request with title,
        should return 201 and create
        """
        self.client.login(username='FirstTester', password='pass')
        response = self.client.post(
            '/goals/', {"title": "title", "focus": 1})
        print(response)
        count = Goal.objects.count()
        self.assertEqual(count, 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

