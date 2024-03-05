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
        

class FocusDetailViewTests(APITestCase):
    """
    Tests for the Focus Detail view
    """
    def setUp(self):
        FirstTester = User.objects.create_user(username='FirstTester', password='pass')
        Focus.objects.create(
            owner=FirstTester, name="Name", why="Why"
        )
        SecondTester = User.objects.create_user(username='SecondTester', password='word')
        Focus.objects.create(
            owner=SecondTester, name="Test", why="To test"
        )
    
    def test_logged_in_can_get_their_focus_detail(self):
        """
        Logged in user sending a get request for a focus they own, should return focus
        """
        self.client.login(username='FirstTester', password='pass')
        response = self.client.get('/focus/1')
        focus = response.data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(focus['owner'], 'FirstTester')
        self.assertEqual(focus['name'], 'Name')

    def test_logged_out_no_access_focus_detail(self):
        """
        Logged out user sending a get request for a focus, should return access denied
        """
        response = self.client.get('/focus/1')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_invalid_focus_request_handled(self):
        """
        Logged in user sending a get request for a focus that doesn't exist, should return 404 not found
        """
        self.client.login(username='FirstTester', password='pass')
        response = self.client.get('/focus/3')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_logged_in_denied_get_focus_dont_own(self):
        """
        Logged in user sending get request for focus they don't own, should return access denied
        """
        self.client.login(username='FirstTester', password='pass')
        response = self.client.get('/focus/2')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_logged_in_owner_can_edit_their_focus(self):
        """
        Logged in user sending a put request for owned focus, should return ok and make changes
        """
        self.client.login(username='FirstTester', password='pass')
        response = self.client.put('/focus/1', {'name': 'name changed'})
        focus = response.data
        self.assertEqual(focus['name'], 'name changed')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_logged_in_owner_denied_edit_focus_dont_own(self):
        """
        Logged in user sending a put request for focus they dont own, should return access denied
        """
        self.client.login(username='FirstTester', password='pass')
        response = self.client.put('/focus/2', {'name': 'name changed'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)  

    def test_logged_in_owner_can_delete_their_focus(self):
        """
        Logged in user sending a delete request for owned focus, should return ok and delete focus
        """
        self.client.login(username='FirstTester', password='pass')
        response = self.client.delete('/focus/1')
        count = Focus.objects.count()
        self.assertEqual(count, 1)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_logged_in_owner_denied_delete_focus_dont_own(self):
        """
        Logged in user sending a delete request for focus they don't own, should return access denied
        """
        self.client.login(username='FirstTester', password='pass')
        response = self.client.delete('/focus/2')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)