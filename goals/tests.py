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
        """
        Create two users, each with one focus. The second user also has one goal.
        """
        first_tester = User.objects.create_user(
            username='FirstTester', password='pass')
        Focus.objects.create(
            owner=first_tester, name="Name", why="Why"
        )
        second_tester = User.objects.create_user(
            username='SecondTester', password='word')
        second_tester_focus = Focus.objects.create(
            owner=second_tester, name="Test", why="So the second user also has a focus"
        )
        Goal.objects.create(
            owner=second_tester, title='Second Testers goal', focus=second_tester_focus
        )

    def test_logged_out_no_create_goal(self):
        """
        Not logged in user sending HTTP post request, should return 403 error
        """
        response = self.client.post(
            '/goals/', {"title": "title", "focus": 1})
        count = Goal.objects.count()
        self.assertEqual(count, 1)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_logged_in_can_create_goal(self):
        """
        Logged in user sending a post request with title,
        should return 201 and create
        """
        self.client.login(username='FirstTester', password='pass')
        response = self.client.post(
            '/goals/', {"title": "title", "focus": 1})
        count = Goal.objects.count()
        self.assertEqual(count, 2)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_goal_create_no_title_throws_error(self):
        """
        Logged in user sending post request without name data,
        should return 400 error
        """
        self.client.login(username='FirstTester', password='pass')
        response = self.client.post(
            '/goals/', {"focus": 1})
        count = Goal.objects.count()
        self.assertEqual(count, 1)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_logged_out_no_view_goal_list(self):
        """
        Not logged in user sending HTTP get request, should recieve 403 error
        """
        response = self.client.get('/goals/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_view_own_goals_only(self):
        """
        Logged in user sending get request, receives only their goals
        """
        self.client.login(username='FirstTester', password='pass')
        self.client.post('/goals/', {"title": "title", "focus": 1})
        response = self.client.get('/goals/')
        number_goals_returned = response.data['count']
        number_goals = Goal.objects.count()
        results = response.data['results']
        goal_owner = results[0]['owner']
        self.assertEqual(number_goals, 2)
        self.assertEqual(number_goals_returned, 1)
        self.assertEqual(goal_owner, 'FirstTester')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_filter_by_parent_is_none(self):
        """
        Logged in user can request only goals with no parent
        """
        self.client.login(username='SecondTester', password='word')
        self.client.post('/goals/', {"title": "nested goal", "focus": 2, "parent": 1})
        response = self.client.get('/goals/?parent=None')
        number_goals_returned = response.data['count']
        results = response.data['results']
        title = results[0]['title']
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(number_goals_returned, 1)
        self.assertEqual(title, 'Second Testers goal')

    def test_filter_by_parent_id(self):
        """
        Logged in user can request children goals of a specified parent
        """
        self.client.login(username='SecondTester', password='word')
        self.client.post('/goals/', {"title": "nested goal", "focus": 2, "parent": 1})
        response = self.client.get('/goals/?parent_id=1')
        number_goals_returned = response.data['count']
        results = response.data['results']
        title = results[0]['title']
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(number_goals_returned, 1)
        self.assertEqual(title, 'nested goal')
