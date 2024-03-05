# Testing and Validation

## Contents

[Code Validation](#code-validation)

[Manual Testing](#manual-testing)

[Automated Testing](#automated-testing)

---

## Code Validation

[Return to contents list](#contents)

## Manual Testing

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
