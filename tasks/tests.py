from django.contrib.auth.models import User
from .models import Task
from goals.models import Goal
from focus.models import Focus
from rest_framework import status
from rest_framework.test import APITestCase


class TaskListViewTests(APITestCase):
    """
    Tests for the Task list view
    """
    def setUp(self):
        """
        Create two users, each with a focus, a goal, and
        three tasks (1 miscellaneous, 1 focus day-to-day and 1 goal steps)
        """
        first_tester = User.objects.create_user(
            username='FirstTester', password='pass')
        first_tester_focus = Focus.objects.create(
            owner=first_tester, name="First tester's focus", why="Why"
        )
        first_tester_goal = Goal.objects.create(
            owner=first_tester,
            title='First testers goal',
            focus=first_tester_focus,
            active=True
        )
        Task.objects.create(
            owner=first_tester,
            name="First miscellaneous today achieved",
            today=True,
            achieved=True
        )
        Task.objects.create(
            owner=first_tester,
            name="First focus today",
            focus=first_tester_focus,
            today=True
        )
        Task.objects.create(
            owner=first_tester,
            name="First active goal backlog only",
            focus=first_tester_focus,
        )

        second_tester = User.objects.create_user(
            username='SecondTester', password='word')
        second_tester_focus = Focus.objects.create(
            owner=second_tester,
            name="Second testers focus",
            why="why"
        )
        second_tester_goal = Goal.objects.create(
            owner=second_tester,
            title='Second Testers goal',
            focus=second_tester_focus
        )
        Task.objects.create(
            owner=second_tester,
            name="Second miscellaneous backlog only"
        )
        Task.objects.create(
            owner=second_tester,
            name="Second focus today achieved",
            focus=second_tester_focus,
            today=True,
            achieved=True
        )
        Task.objects.create(
            owner=second_tester,
            name="Second paused goal",
            focus=second_tester_focus,
            goal=second_tester_goal
        )

    def test_logged_out_no_create_task(self):
        """
        Not logged in user sending HTTP post request, should return 403 error
        """
        response = self.client.post(
            '/tasks/', {"name": "title"})
        count = Task.objects.count()
        self.assertEqual(count, 6)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_logged_in_can_create_task(self):
        """
        Logged in user sending a post request with name,
        should return 201 and create
        """
        self.client.login(username='FirstTester', password='pass')
        response = self.client.post(
            '/tasks/', {"name": "name"})
        count = Task.objects.count()
        self.assertEqual(count, 7)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_logged_out_no_view_task_list(self):
        """
        Not logged in user sending a get request should recieve 403 error
        """
        response = self.client.get('/tasks/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_view_own_tasks_only(self):
        """
        Logged in user sending get request, receives only their tasks
        """
        self.client.login(username='FirstTester', password='pass')
        response = self.client.get('/tasks/')
        number_tasks_returned = response.data['count']
        results = response.data['results']
        task_owner = results[0]['owner']
        self.assertEqual(number_tasks_returned, 3)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
