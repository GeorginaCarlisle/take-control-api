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

[Return to contents list](#contents)
