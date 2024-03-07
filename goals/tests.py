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
        Create two users, each with one focus.
        The second user also has one goal.
        """
        first_tester = User.objects.create_user(
            username='FirstTester', password='pass')
        Focus.objects.create(
            owner=first_tester, name="Name", why="Why"
        )
        second_tester = User.objects.create_user(
            username='SecondTester', password='word')
        second_tester_focus = Focus.objects.create(
            owner=second_tester,
            name="Test",
            why="So the second user also has a focus"
        )
        Goal.objects.create(
            owner=second_tester,
            title='Second Testers goal',
            focus=second_tester_focus
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
        self.client.post(
            '/goals/', {"title": "nested goal", "focus": 2, "parent": 1})
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
        self.client.post(
            '/goals/', {"title": "nested goal", "focus": 2, "parent": 1})
        response = self.client.get('/goals/?parent_id=1')
        number_goals_returned = response.data['count']
        results = response.data['results']
        title = results[0]['title']
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(number_goals_returned, 1)
        self.assertEqual(title, 'nested goal')


class GoalDetailViewTests(APITestCase):
    """
    Tests for the Goal detail view
    """

    def setUp(self):
        """
        Create two users, each with one focus and one goal.
        """
        first_tester = User.objects.create_user(
            username='FirstTester', password='pass')
        first_tester_focus = Focus.objects.create(
            owner=first_tester, name="Name", why="Why"
        )
        Goal.objects.create(
            owner=first_tester,
            title='First Testers goal',
            focus=first_tester_focus
        )
        second_tester = User.objects.create_user(
            username='SecondTester', password='word')
        second_tester_focus = Focus.objects.create(
            owner=second_tester,
            name="Test",
            why="So the second user also has a focus"
        )
        Goal.objects.create(
            owner=second_tester,
            title='Second Testers goal',
            focus=second_tester_focus
        )

    def test_logged_out_no_access_goal_detail(self):
        """
        Logged out user sending a get request for a goal,
        should recieve access denied
        """
        response = self.client.get('/goals/1')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_logged_in_can_get_their_goal(self):
        """
        Logged in user sending a get request for a goal they own,
        should return goal
        """
        self.client.login(username='FirstTester', password='pass')
        response = self.client.get('/goals/1')
        goal = response.data
        title = goal['title']
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(title, 'First Testers goal')

    def test_logged_in_denied_goal_dont_own(self):
        """
        Logged in user sending get request for goal they don't own,
        should return access denied
        """
        self.client.login(username='FirstTester', password='pass')
        response = self.client.get('/goals/2')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_invalid_goal_request_handled(self):
        """
        Logged in user sending a get request for a goal that doesn't exist,
        should return 404 not found
        """
        self.client.login(username='FirstTester', password='pass')
        response = self.client.get('/goals/3')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_logged_in_owner_can_edit_their_goal(self):
        """
        Logged in user sending a patch request for owned goal,
        should return ok and make changes
        """
        self.client.login(username='FirstTester', password='pass')
        response = self.client.patch('/goals/1', {'title': 'name changed'})
        goal = response.data
        title = goal['title']
        self.assertEqual(title, 'name changed')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_logged_in_owner_denied_edit_goal_dont_own(self):
        """
        Logged in user sending a patch request for goal they dont own,
        should return access denied
        """
        self.client.login(username='FirstTester', password='pass')
        response = self.client.patch('/goals/2', {'title': 'name changed'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_logged_in_owner_can_delete_their_goal(self):
        """
        Logged in user sending a delete request for owned goal,
        should return ok and delete focus
        """
        self.client.login(username='FirstTester', password='pass')
        response = self.client.delete('/goals/1')
        count = Goal.objects.count()
        self.assertEqual(count, 1)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_logged_in_owner_denied_delete_goal_dont_own(self):
        """
        Logged in user sending a delete request for goal they don't own,
        should return access denied
        """
        self.client.login(username='FirstTester', password='pass')
        response = self.client.delete('/goals/2')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
