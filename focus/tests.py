from django.contrib.auth.models import User
from .models import Focus
from rest_framework import status
from rest_framework.test import APITestCase

class FocusListViewTests(APITestCase):
    """
    Tests for the Focus List view
    """
    def setUp(self):
        User.objects.create_user(username='FirstTester', password='pass')
    
    def test_logged_out_no_create_focus(self):
        """
        Not logged in user sending HTTP post request, should return 403 error
        """
        response = self.client.post('/focus/', {"name":"a name", "why":"why"})
        count = Focus.objects.count()
        self.assertEqual(count, 0)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_logged_out_no_view_focus_list(self):
        """
        Not logged in user sending HTTP get request, should return 403 error
        """
        response = self.client.get('/focus/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_logged_in_can_create_focus(self):
        """
        Logged in user sending a post request with name and why, should return 201 and create
        """
        self.client.login(username='FirstTester', password='pass')
        response = self.client.post('/focus/', {"name":"a name", "why":"why"})
        count = Focus.objects.count()
        self.assertEqual(count, 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_focus_create_no_name_throws_error(self):
        """
        Logged in user sending post request without name data, should return 400 error
        """
        self.client.login(username='FirstTester', password='pass')
        response = self.client.post('/focus/', {"why":"why"})
        count = Focus.objects.count()
        self.assertEqual(count, 0)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
         
    def test_focus_view_own_focus_only(self):
        """
        Logged in user sending get request, receives only their focuses
        """
        SecondTester = User.objects.create_user(username='SecondTester', password='word')
        Focus.objects.create(
            owner=SecondTester, name="Test", why="To test"
        )
        self.client.login(username='FirstTester', password='pass')
        self.client.post('/focus/', {"name":"a name", "why":"why"})
        response = self.client.get('/focus/')
        count = response.data['count']
        results = response.data['results']
        focusOwner = results[0]['owner'] 
        self.assertEqual(count, 1)
        self.assertEqual(focusOwner, 'FirstTester')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        

