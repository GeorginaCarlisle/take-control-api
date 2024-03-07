# Testing and Validation

## Contents

[Code Validation](#code-validation)

[Manual Testing](#manual-testing)

[Automated Testing](#automated-testing)

---

## Code Validation

All code has been passed through a Python Linter.

| App | file | outcome |
| --- | --- | --- |
| focus | models.py | No errors |
| | serializers.py | No errors |
| | tests.py | No errors |
| | urls.py | No errors |
| |  views.py | No errors |
| goal | models.py | No errors |
| | serializers.py | No errors |
| | tests.py | No errors |
| | urls.py | No errors |
| |  views.py | No errors |

[Return to contents list](#contents)

## Manual Testing

Manual tests for all Endpoints have been carried out on the deployed site.

### Authorisation

| url | http request | expected outcome | result |
| --- | --- | --- | --- |
| dj-rest-auth/registration/ | POST | New user created | 500 server error thrown. Database correctly updated with new user. |
| | | Invalid fields handled | PASS |
| dj-rest-auth/login/ | POST | User Authenticated | PASS |
| | | Invalid fields handled | PASS |
| dj-rest-auth/logout/ | POST | User logged out and token object deleted | PASS |

Key notes:
While registration updates the database correctly a 500 error is thrown. See bug #1 in main readme.

### Focus model

| url | http request | expected outcome | result |
| --- | --- | --- | --- |
| focus/ | GET | Unauthorized error for logged out users | PASS |
| | | list of all logged in user's focus area and non of anyone elses | PASS |
| | | focus areas ordered by rank first and then by created_at in ascending order | PASS |
| | POST | Unauthorized error for logged out users | PASS |
| | | Error message for empty name field | PASS |
| | | Error message for name over 50 characters | PASS|
| | | Error message for images too large | PASS |
| | | new focus created for logged in user | PASS |
| focus/<int:pk> | GET | Invalid focus request returns 404 | PASS |
| | | Logged in user can get their focus | PASS |
| | | Logged in user trying to get a focus that doesn't belong to them returns 403 error | PASS |
| | | Logged out user cannot make get request 401 error | PASS |
| | PUT | Logged in user can edit their focus | Fail in deployed API |
| | DELETE | Logged in user can delete their focus | Fail in deployed API |

Key notes:
Walkthrough api, which works correctly from frontend also fails in the same way.

[Return to contents list](#contents)

## Automated Testing

Automated tests have been created for all views

### FocusListView

| Test name | Description | Outcome |
| --- | ---- | -- |
| test_logged_out_no_create_focus | Not logged in user sending HTTP post request, should return 403 error | Pass |
| test_logged_out_no_view_focus_list | Not logged in user sending HTTP get request, should return 403 error | Pass |
| test_logged_in_can_create_focus | Logged in user sending a post request with name and why, should return 201 and create new focus | Pass |
| test_focus_create_no_name_throws_error | Logged in user sending post request without name data, should return 400 error | Pass |
| test_focus_view_own_focus_only | Logged in user sending get request, receives only their focuses | Pass |

### FocusDetailView

| Test name | Description | Outcome |
| --- | ---- | -- |
| test_logged_in_can_get_their_focus_detail | Logged in user sending a get request for a focus they own, should return focus | Pass |
| test_logged_out_no_access_focus_detail | Logged out user sending a get request for a focus, should return access denied | Pass |
| test_invalid_focus_request_handled | Logged in user sending a get request for a focus that doesn't exist, should return 404 not found | Pass |
| test_logged_in_denied_get_focus_dont_own | Logged in user sending get request for focus they don't own, should return access denied | Pass |
| test_logged_in_owner_can_edit_their_focus | Logged in user sending a put request for owned focus, should return ok and make changes | Pass |
| test_logged_in_owner_denied_edit_focus_dont_own | Logged in user sending a put request for focus they dont own, should return access denied | Pass |
| test_logged_in_owner_can_delete_their_focus | Logged in user sending a delete request for owned focus, should return ok and delete focus | Pass |
| test_logged_in_owner_denied_delete_focus_dont_own | Logged in user sending a delete request for focus they don't own, should return access denied | Pass |

[Return to contents list](#contents)
