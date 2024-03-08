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
            goal=first_tester_goal,
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
            goal=second_tester_goal,
            active=False
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
        self.assertEqual(task_owner, 'FirstTester')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_filter_tasks_by_active(self):
        """
        Logged in user can request only their active tasks
        """
        self.client.login(username='SecondTester', password='word')
        response = self.client.get('/tasks/?active=True')
        number_tasks_returned = response.data['count']
        self.assertEqual(number_tasks_returned, 2)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_filter_tasks_by_today(self):
        """
        Logged in user can request only their today tasks
        """
        self.client.login(username='SecondTester', password='word')
        response = self.client.get('/tasks/?today=True')
        number_tasks_returned = response.data['count']
        results = response.data['results']
        task_name = results[0]['name']
        self.assertEqual(task_name, 'Second focus today achieved')
        self.assertEqual(number_tasks_returned, 1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_filter_tasks_by_achieved(self):
        """
        Logged in user can request only their achieved tasks
        """
        self.client.login(username='SecondTester', password='word')
        response = self.client.get('/tasks/?achieved=True')
        number_tasks_returned = response.data['count']
        results = response.data['results']
        task_name = results[0]['name']
        self.assertEqual(task_name, 'Second focus today achieved')
        self.assertEqual(number_tasks_returned, 1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_filter_by_miscellaneous(self):
        """
        Logged in user can request only their tasks with no focus
        """
        self.client.login(username='SecondTester', password='word')
        response = self.client.get('/tasks/?focus=None')
        number_tasks_returned = response.data['count']
        results = response.data['results']
        task_name = results[0]['name']
        self.assertEqual(task_name, 'Second miscellaneous backlog only')
        self.assertEqual(number_tasks_returned, 1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_filter_by_focus_day_to_day(self):
        """
        Logged in user can request all the day-to-day tasks from
        one of their focus areas
        """
        self.client.login(username='SecondTester', password='word')
        response = self.client.get('/tasks/?focus=2')
        number_tasks_returned = response.data['count']
        results = response.data['results']
        task_name = results[0]['name']
        self.assertEqual(task_name, 'Second focus today achieved')
        self.assertEqual(number_tasks_returned, 1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_filter_by_goal(self):
        """
        Logged in user can request all tasks linked to a goal
        """
        self.client.login(username='SecondTester', password='word')
        response = self.client.get('/tasks/?goal=2')
        number_tasks_returned = response.data['count']
        results = response.data['results']
        task_name = results[0]['name']
        self.assertEqual(task_name, 'Second paused goal')
        self.assertEqual(number_tasks_returned, 1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class TaskDetailViewTests(APITestCase):
    """
    Tests for the Task Detail view
    """
    def setUp(self):
        """
        Create two users, each with a task
        """
        first_tester = User.objects.create_user(
            username='FirstTester', password='pass')
        Task.objects.create(
            owner=first_tester,
            name="First miscellaneous today achieved",
            today=True,
            achieved=True
        )
        second_tester = User.objects.create_user(
            username='SecondTester', password='word')
        Task.objects.create(
            owner=second_tester,
            name="Second miscellaneous backlog only"
        )

    def test_logged_out_no_access_task_detail(self):
        """
        Logged out user sending a get request for a task,
        should recieve access denied
        """
        response = self.client.get('/tasks/1')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_logged_in_can_get_their_task(self):
        """
        Logged in user sending a get request for a task they own,
        should return task
        """
        self.client.login(username='FirstTester', password='pass')
        response = self.client.get('/tasks/1')
        task = response.data
        owner = task['owner']
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(owner, 'FirstTester')

    def test_logged_in_denied_task_dont_own(self):
        """
        Logged in user sending get request for task they don't own,
        should return access denied
        """
        self.client.login(username='FirstTester', password='pass')
        response = self.client.get('/tasks/2')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_invalid_task_request_handled(self):
        """
        Logged in user sending a get request for a task that doesn't exist,
        should return 404 not found
        """
        self.client.login(username='FirstTester', password='pass')
        response = self.client.get('/tasks/3')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_logged_in_owner_can_edit_their_task(self):
        """
        Logged in user sending a patch request for owned task,
        should return ok and make changes
        """
        self.client.login(username='FirstTester', password='pass')
        response = self.client.patch('/tasks/1', {'name': 'name changed'})
        task = response.data
        name = task['name']
        self.assertEqual(name, 'name changed')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_logged_in_owner_denied_edit_task_dont_own(self):
        """
        Logged in user sending a patch request for task they dont own,
        should return access denied
        """
        self.client.login(username='FirstTester', password='pass')
        response = self.client.patch('/tasks/2', {'name': 'name changed'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_logged_in_owner_can_delete_their_task(self):
        """
        Logged in user sending a delete request for owned task,
        should return ok and delete task
        """
        self.client.login(username='FirstTester', password='pass')
        response = self.client.delete('/tasks/1')
        count = Task.objects.count()
        self.assertEqual(count, 1)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_logged_in_owner_denied_delete_task_dont_own(self):
        """
        Logged in user sending a delete request for task they don't own,
        should return access denied
        """
        self.client.login(username='FirstTester', password='pass')
        response = self.client.delete('/tasks/2')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
