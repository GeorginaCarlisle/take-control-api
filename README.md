# Take Control API

Developer: Georgina Carlisle

An API providing full CRUD functionality for task management data that includes setting focus areas and goals. This API utilises the Django Rest Framework and was created to provide backend functionality for the Take Control application.

[Take Control API live link](https://take-control-api-d106d6135431.herokuapp.com/)
[Take Control App repository](https://github.com/GeorginaCarlisle/take-control-frontend-app)
Take Control App live link:

## Contents

[Features](#features)

[Design](#design)

[Agile Methodology](#agile-methodology)

[Languages](#languages)

[Frameworks and Libraries](#frameworks-and-libraries)

[Tools and Technologies](#tools-and-technologies)

[Testing and Validation](#testing-and-validation)

[Bugs and Fixes](#bugs-and-fixes)

[Deployment](#deployment)

[Cloning this repository](#cloning-this-repository)

[Forking a branch](#forking-a-branch)

[Credits](#credits)

[Acknowledgements](#acknowledgements)

---

## Features

### Security

Only the following can be accessed by none authenticated users, all other endpoints can only be accessed if authorised:

- The base root, which gives a welcome message
- The /dj-rest-auth/registration/ endpoint, which allows new users to register.
- The /dj-rest-auth/login/ endpoint, which allows users to login

Only owners of a data instance can access any CRUD functionality related to it. All get requests returning a list will only return items for which the user is the owner. Any requests for a specific item that the user doesn't own will be denied.

### User Model

Users can register, login and logout.

| Field | Automatic/required/optional | Notes |
| --- | ---- | ---- |
| username | required | Must be unique |
| email | required | Must be unique and a valid format |
| password | required | Must pass complexity rules to prevent common or easily guessable passwords |

Endpoints for the user model:

| url | notes |
| --- | --- |
| dj-rest-auth/registration/ | register a new user account |
| dj-rest-auth/login/ | Login to account |
| dj-rest-auth/logout/ | Logout of account |

### Focus Model

Users can store focus areas - areas of their life which they would like to focus on. These can be given a 'why' reason, an image and a rank.

Fields held within the database:

| Field | Automatic/required/optional | Notes |
| --- | ---- | ---- |
| owner | automatically generated | Foreign key link to a user instance |
| created_at | automatically generated | DateTime |
| updated_at | automatically generated | DateTime |
| name | required | text of max characters 50 |
| rank | optional | integer |
| why | optional | text |
| image | default provided if non given | stored in cloudinary, only images smaller than 2MBS, height: 4096 and width: 4096 will be accepted |

Extra fields generated and returned with a GET request:

- Is owner field, which will return true if the authorised user is the owner

Endpoints for the focus model:

| url | http request | notes |
| --- | --- | --- |
| focus/ | GET | Returns a list of user's focus areas ordered by rank first and then by created_at |
| focus/ | POST | Create a new focus area |
| focus/id | GET | Get a specific focus area using it's id |
| focus/id | PUT | Update a focus area. All details needed |
| focus/id | PATCH | update a field within a focus area. |
| focus/id | DELETE | Delete a focus area using it's id |

### Goal Model

Users can store their goals. These must be linked to a focus area. Goals can be given a description, value to be gained, success criteria and deadline. They can be toggled as active or not. Goals may be nested inside each other providing the option to break large goals up into smaller ones.

Fields held within the database:

| Field | Automatic/required/optional | Notes |
| --- | ---- | ---- |
| owner | automatically generated | Foreign key link to a user instance |
| focus | required | Foreign key link to a focus instance. Input focus id |
| children | default: false | Set as true if this goal has nested goals |
| parent | optional | Foreign key link to a goal instance providing a way to nest one goal inside another |
| created_at | automatically generated | DateTime |
| updated_at | automatically generated | DateTime |
| active | default: true | set as false to pause goal |
| deadline | optional | DateTime |
| title | required | text of max characters 50 |
| description | optional | text of max characters 100 |
| value | optional | text of max characters 100 |
| criteria | optional | text of max characters 100 |

Extra fields generated and returned with a GET request:

- is_owner field, which will return true if the authorised user is the owner
- days_remaining field, which will return the number of days remaining until the deadline.
- deadline_near, which will return true if the deadline is less than 7 days away.

Endpoints for the goal model. Note multiple filter and ordering options can be given together. Example: goals/?focus_id=<>&parent=None :

| url | http request | notes |
| --- | --- | --- |
| goals/ | GET | Returns a list of user's focus areas ordered by deadline first and then by created_at |
| goals/?parent=None | GET | Returns a list of all the user's goals without a parent (aren't nested) |
| goals/?parent_id=<> | GET | Returns a list of all user's goals which are nested in a given parent |
| goals/?focus_id=<> | GET | Returns a list of all user's goals with given focus |
| goals/ | POST | Create a new focus area |
| goals/id | GET | Get a specific focus area using it's id |
| goals/id | PUT | Update a focus area. All details needed |
| goals/id | PATCH | update a field within a focus area. |
| goals/id | DELETE | Delete a focus area using it's id |

### Task Model

Users can store their tasks. Tasks can be linked directly to a focus, to a goal or be unlinked. Tasks can be given a description and have the following set as true or false: active, today or achieved. A number of extra fields are also returned with a task. Multiple options for filtering and ordering are included.

Fields held within the database:

| Field | Automatic/required/optional | Notes |
| --- | ---- | ---- |
| owner | automatically generated | Foreign key link to a user instance |
| focus | optional | Foreign key link to a focus instance. Input focus id |
| goal | optional | Foreign key link to a goal instance. Input goal id |
| created_at | automatically generated | DateTime |
| updated_at | automatically generated | DateTime |
| active | default: true | can change to false |
| today | default: false | can change to true |
| achieved | default: false | can change to true |
| deadline | optional | DateTime |
| name | required | text of max characters 100 |

Extra fields generated and returned with a GET request:

- is_owner field, which will return true if the authorised user is the owner.
- deadline_info, which calculates if the task is overdue, due today or due tomorrow.
- goal_deadline_info, which brings in the deadline of a linked goal and calculates if it is overdue, due today or due tomorrow.
- context, which details clearly how the task is linked.

Endpoints for the task model. Note multiple filter and ordering options can be given together:

| url | http request | notes |
| --- | --- | --- |
| tasks/ | GET | Returns a list of user's tasks ordered by deadline first and then by created_at |
| tasks/?active=True | GET | Returns a list of all the user's active tasks |
| tasks/?active=False | GET | Returns a list of all the user's non-active tasks |
| tasks/?today=True | GET | Returns a list of all user's today tasks |
| tasks/?today=False | GET | Returns a list of all user's tasks not marked as today |
| tasks/?achieved=True | GET | Returns a list of all user's achieved tasks |
| tasks/?achieved=False | GET | Returns a list of all user's tasks not marked as achieved |
| tasks/?focus=None | GET | List all user's miscellaneous tasks |
| tasks/?focus=id | GET | List all user's tasks for a given focus |
| tasks/?goal=None | GET | List all user's tasks without a goal |
| tasks/?goal=id | GET | List all user's tasks for a given goal |
| tasks/?ordering=updated_at | GET | List all user's tasks in order of updated_at |
| tasks/?ordering=focus__rank | GET | List all user's tasks in order of thier linked focus rank |
| tasks/?ordering=goal__deadline | GET | List all user's tasks in order of their linked goal's deadline |
| tasks/?ordering=deadline | GET | List all user's tasks in order of deadline |
| tasks/?ordering=created_at | GET | List all user's tasks in order of created_at |
| tasks/ | POST | Create a new task |
| tasks/id | GET | Get a specific task using it's id |
| tasks/id | PUT | Update a focus area. All details needed |
| tasks/id | PATCH | update a field within a focus area. |
| tasks/id | DELETE | Delete a focus area using it's id |

[Return to contents list](#contents)

## Design

### Aim

To store task management data that includes setting focus areas, goals and tasks, and provide a full range of CRUD functionality to any linked applications.

### Safety Considerations

Only trusted urls, specified directly within the API, will be able to make requests to the API and access any CRUD functionality.

User authentication will be included within the API, with read, update and delete functionality initially only available to the owner of the data. Later functionality will allow for access to be granted to team member users.

Secret keys etc. will be hidden and Debug set to False for the deployed api.

### Scope

The scope of this API links directly to the user stories set out in the Take Control repository. From these the following key models were defined:

- User (In-built Django user model)
- Focus
- Goal
- Task
- Label

### Structure

The following documents show planning for the models, including extra helper models needed, as well as planning for all endpoints including associated serializers, permissions and views. These plans were developed in parallel with the scope, structure and skeleton design planes for the linked application.

Please note that the end point plan does not contain endpoints for the team and permissions models shown in the model plan. The associated functionality was prioritised as a could-have, with further planning to be completed only following completion of all must-have and should-have functionality and should time allow.

[Model Plan](documentation/api-model-plan.pdf)

[Endpoint Plan](documentation/api-endpoint-plan.pdf)

[Return to contents list](#contents)

## Agile Methodology

Agile values and principles were followed in the creation of this API in partnership with the [Take Control Application](https://github.com/GeorginaCarlisle/take-control-frontend-app).

### Prioritisation

As both the API and application were to be built in tandom, the decision was made to chunk the endpoints needed from the api by MOSCOW prioritisation.

Each chunk was then fully completed before moving onto building the associated Epics within the application. Once all the associated must-haves and any none api dependent must-haves were completed a decision was taken in view of time how many should-haves and could-haves to complete. Only then did I returned to working on the api to build the next chunk.

Must Have:

- Framework set-up
- Authorisation endpoints and JSON tokens
- Focus model and endpoints
- Goal model and endpoints
- Task model and endpoints

Should have:

- Label model and endpoints
- Repeated model and endpoints
- Order model and endpoints

Could have:

- Team model and endpoints, plus any changes now needed to other endpoints
- Permissions model and endpoints, plus any changes now needed to other endpoints

### Information Radiator

Githubs project board was used to keep track of tasks to be completed, with github issues used to define key tasks. Tasks were then given success criteria and further split up into smaller tasks.

The project board was also shared by the [Take Control App repository](https://github.com/GeorginaCarlisle/take-control-frontend-app). This allowed both frontend and backend tasks to be viewed together and worked on in an order that allowed me to push for the best overall product that could be achieved within the time frame.

### Time Boxing

Developement of the project was split into four time boxes/iterations. Each iteration was set to a period of one week and had a set focus. This allowed for judgements to be made for each task as to how far to push perfection and how quickly to move on, so that I was able to bring the project together into a finished state prior to the deadline. [See details in the frontend repository](https://github.com/GeorginaCarlisle/take-control-frontend-app?tab=readme-ov-file#agile-methodology).

[Return to contents list](#contents)

## Languages

Python

## Frameworks and Libraries

[Django 3.2](https://www.djangoproject.com/) - A high-level Python web framework that encourages rapid development and clean, pragmatic design.

[Django Rest Framework 3.14](https://www.django-rest-framework.org/) - A powerful a flexible toolkit for building Web APIs.

[dj_database_url 2.1](https://pypi.org/project/dj-database-url/) - A simple Django utility. Used to configure the API to connect up to an outside database using it's URL.

[Psycopg2-binary 2.9](https://pypi.org/project/psycopg2-binary/) - A PostgreSQL database adapter for the Python programming language. The stand-alone binary package was chosen due to the normal psycopg2 throwing errors.

[Gunicorn 21.2](https://gunicorn.org/) - A Python WSGI HTTP Server for UNIX.

[Cloudinary 1.39 and Cloudinary storage 0.3](https://cloudinary.com/) - Allowing connection with Cloudinary (see tools and tech).

[Pillow 8.2](https://pypi.org/project/pillow/8.2.0/) - A Python imaging library that includes image processing capabilities.

[django-cors-headers 4.3](https://pypi.org/project/django-cors-headers/) - A Django application for handling the server headers required for Cross-Origin Resource Sharing (CORS)

[dj-rest-auth package 2.1](https://dj-rest-auth.readthedocs.io/en/latest/installation.html) - A set of REST API endpoints to handle User Registration and Authentication tasks.

[djangorestframework-simplejwt package 4.7](https://pypi.org/project/djangorestframework-simplejwt/) - A JSON Web Token authentication plugin for the Django REST Framework.

[Return to contents list](#contents)

## Tools and Technologies

[Code Institute Template](https://github.com/Code-Institute-Org/ci-full-template) - Provided me with a familiar base from which to build my project.

[GitHub](https://github.com/)  - Stores the repository for this project so that it can be viewed by others. Github issues and projects were also utilised, see [Agile Methodology](#agile-methodology).

[git](https://git-scm.com/) - Controlled the building of this project in a series of versions which can be tracked.

[Visual Studio Code](https://code.visualstudio.com/) - The editor in which this project has been built.

[LucidChart](https://lucid.co/) - Used to plan the models to be included in the database and how they connect together.

[Cloudinary](https://cloudinary.com/) - External API platform used to host images.

[Code Institute database](https://dbs.ci-dbs.net/) - Providing an external PostgreSQL database

[CI Python Linter](https://pep8ci.herokuapp.com/) - Used to validate all the python code.

[Return to contents list](#contents)

## Testing and Validation

See [TESTING.md](TESTING.md) for all testing and validation.

[Return to contents list](#contents)

## Bugs and Fixes

| # | Bug | What was tried | Fix |
| --- | --- | --- | --- |
| 1 | In development mode with local host and db.sqlite3, when registering a new user their is a connection refused error originating in socket.py. Note: Form validation does work and a user is created. | Time was spent checking all related settings and exploring the error code. I also manufactored the same scenario using my walkthrough code (which I know works as expected with the frontend) and it also threw the same error. This led me to the thought that this might be directly connected with the db.sqlite3 database and the local host set-up and may not caused any issues in production. I decided to leave and see what happened on deployment. The deployed API created a new user no problem but threw a 500 error. Deployed walkthrough did the same. | Leave error for now and monitor how registration is handled by frontend. |
| 2 | Default permission 'IsAuthenticated' was preventing unauthenticated users from seeing the root route message and for being able to send a register or login request | First I removed this permission, this solved the initial problem but caused further problems with the list view trying to find a focus for an annoymonous user. I then went back to the django documentation learning about the permission_classes decorators and also the dj-rest-auth documentation. | Default permission reinstated and instead overridden where needed. The root_route overridden with a permission_classes decorator and the AllowAny permission. The registration paths overridden in settings.py within REST_AUTH. This also seemed to fix the login path too. |
| 3 | The FocusListView for the deployed API is returning the list in the complete opposite order to development. | Research suggested that this might be due to how the production and development databases handle ordering differently. | Queryset code in the view changed. Production now correct and development wrong. |
| 4 | Attempting to calculate the difference between datetime.(now) and a date held in the database threw a TypeError: can't subtract offset-naive and offset-aware datetimes. | I researched further about the datetime object learning the difference between naive and aware. I then searched for ways to convert datetime.now into an aware datetime object with the timezone utc, as this was what the timezone of the api is set to. | Use of the replace() method and the sub class tzinfo to give datetime.now() a timezone and make it aware. The caclulation now works without error. |
| 5 | Attempting to pass the image from an instance of the focus model into an additional field created in the task serializer, where the task and the focus shared a foreign key relationship threw the following error: UnicodeDecodeError: 'utf-8' codec can't decode byte 0xff in position 0: invalid start byte | Error traced to the serializer being unable to handle the data stored in the focus models image field. Depsite research I could gain no further understanding or solution. | Decision to handle the required functionality on the frontend for now. |

[Return to contents list](#contents)

## Deployment

This API has been deployed using Heroku.

Instructions to deploy using Heroku:

1 - While in Heroku, navigate to dashboard and then click on the new button in the top right corner choosing: create new app.

2 - Input a name for your app (this name will need to be unique) and choose the correct region for where you are located. Click create app.

3 - Your app has been created, now click on the settings tab.

4 - Click reveal config vars to add any keys the application will need. This project needs:
ALLOWED_HOST, CLIENT_ORIGIN_DEV, CLOUDINARY_URL, DATABASE_URL and any secret keys.

5 - Click on deploy tab. Select deploy method, in this case Git Hub. Confirm connection to git hub by searching for the correct repository and then connecting to it.

6 - To manually deploy project click 'Deploy Branch'. Once built a message will appear saying: Your app was successfully deployed. Click the view button to view the deployed page making a note of it's url.

7 - Don't forget to ensure Debug is false for final deployment.

[Return to contents list](#contents)

## Cloning this repository

In order to work on this repository you will first need to clone it.

Instructions to clone the repository:

1 - While in the GitHub repository, click on the green code button.

2 - Copy the link.

3 - In your IDE or local coding environment use the link to open the repository.

For example: in VScode

clicking on 'Clone Git Repository...' will bring up a box in which to paste the link.
once vscode has the link, you will then be asked where you would like the repo saving.
You should now be set up ready to work on the repository.

For example: in CodeAnywhere

Click on 'Add new workspace'
You will then be given the option to 'Create from your project repository' and a box in which to paste the link
CodeAnywhere will now open a new workspace containing the repository.
You should now be set up ready to work on the repository.

4 - If you are working in VSCode I would then recommend creating a virtual environment:

I use the following command to do this: python3 -m venv .venv
Agreeing to select as workspace folder.
I move into the virutal environment with the command: source .venv/bin/activate

5 - Import all dependencies. I use the command: pip3 install -r requirements.txt.

6 - Create an env.py file in the main directory.

7 - Enter key data, such as: SECRET_KEY, CLIENT_ORIGIN_DEV, CLOUDINARY_URL, DATABASE_URL and ['DEV'] = '1'

8 - Check that both the virtual environment and env.py are named in the .gitignore file.

9 - Check it's all working by running the program. I used the command: python3 manage.py runserver

[Return to contents list](#contents)

## Forking a branch

In order to protect the main branch while you work on something new, essential when working as part of a team or when you want to experiment with a new feature, you will need to fork a branch.

Instructions to fork the repository:

1 - While in the GitHub repository, click on the branch symbol and text indicating the number of branches.

2 - This will load details on current branches. Click on the green 'New branch' button.

3 - Enter a name for the new branch and then click the green 'create new branch' button.

4 - Your new branch should now have appeared on the screen.

5 - Clicking on the new branch and then following the steps for cloning will allow you to open up and work on this branch.

Instructions to fork directly from an issue:

1 - Click to view an issue, either from the issues list or from the project board. From the project board you will need to click once to bring up the issue and then again on the title to go into it fully.

2 - Partway down the right hand side (on desktop) you should see the heading 'Development' and under this a link to 'create a branch for this issue or link a pull request'.

3 - Click on the link to create a forked branch that is tied to the issue.

[Return to contents list](#contents)

## Credits

[Code Institute](https://codeinstitute.net/) - "Django Rest" learning materials followed during the initial set-up of this project, installing dependencies, setting up user registration and authentication, setting up pagination and deploying to Heroku.

### Specific code

The following code from [Code Institute's](https://codeinstitute.net/) Django rest module has been copied and reused within this project:

- validate_image method found in the FocusSerializer

### Images

Image of a person writing in a notebook by [Ylanite Koppens](https://www.pexels.com/photo/person-holding-silver-retractable-pen-in-white-ruled-book-796603/) - has been used as the image associated with all miscellaneous tasks.

Image looking through a camera lens by [Marek](https://www.pexels.com/photo/person-holding-black-camera-lens-339379/) - has been used as the default focus image.

[Return to contents list](#contents)

## Acknowledgements

[Code Institute](https://codeinstitute.net/) - The majority of the coding skills, knowledge and understanding showcased in this project have been learnt through the 'Diploma of Full stack software development' that I am completing with Code Institute.

Django Rest Framework documentation was used throughout the building of this project, in particular to support with:

- [Permissions](https://www.django-rest-framework.org/api-guide/permissions/#permissions) including setting a default permission class and writing a custom permission.
- [Querysets](https://www.django-rest-framework.org/api-guide/viewsets/#modelviewset) and controlling what is being pulled from the database as part of a view.
- [Filtering](https://www.django-rest-framework.org/api-guide/filtering/#filtering) including ordering and filtering.
- [dj-rest-auth](https://dj-rest-auth.readthedocs.io/en/latest/configuration.html) and finding ways around bug #2.

The following documentation was also used:

- [Python datetime documentation](https://docs.python.org/3/library/datetime.html#) to support with understanding the datetime object and how it can be aware and naive.

- [Python - datetime.tzinfo()](https://www.geeksforgeeks.org/python-datetime-tzinfo/) to also support with understanding the datetime object.

[Return to contents list](#contents)
