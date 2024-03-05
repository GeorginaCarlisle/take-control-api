# Take Control API

Developer: Georgina Carlisle

An API providing full CRUD functionality for task management data that includes setting focus areas and goals. This API utilises the Django Rest Framework and was created to provide backend functionality for the Take Control application.

Take Control API live link:
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

[Return to contents list](#contents)

## Testing and Validation

See [TESTING.md](TESTING.md) for all testing and validation.

[Return to contents list](#contents)

## Bugs and Fixes

| # | Bug | What was tried | Fix |
| --- | --- | --- | --- |
| 1 | In development mode with local host and db.sqlite3, when registering a new user their is a connection refused error originating in socket.py. Note: Form validation does work and a user is created. | Time was spent checking all related settings and exploring the error code. I also manufactored the same scenario using my walkthrough code (which I know deploys well and works as expected with the frontend) and it also threw the same error. This has lead me to the thought that this might be directly connected with the db.sqlite3 database and the local host set-up and may not caused any issues in production. | Leave error for now. If any issues are caused with the deployed API and external database I will then re-explore what is causing the error. |
| 2 | Default permission 'IsAuthenticated' was preventing unauthenticated users from seeing the root route message and for being able to send a register or login request | First I removed this permission, this solved the initial problem but caused further problems with the list view trying to find a focus for an annoymonous user. I then went back to the django documentation learning about the permission_classes decorators and also the dj-rest-auth documentation. | Default permission reinstated and instead overridden where needed. The root_route overridden with a permission_classes decorator and the AllowAny permission. The registration paths overridden in settings.py within REST_AUTH. This also seemed to fix the login path too. |
| 3 | The FocusListView for the deployed API is returning the list in the complete opposite order to development. | Research suggested that this might be due to how the production and development databases handle ordering differently. | Queryset code in the view changed. Production now correct and development wrong. |

[Return to contents list](#contents)

## Deployment

[Return to contents list](#contents)

## Cloning this repository

[Return to contents list](#contents)

## Forking a branch

[Return to contents list](#contents)

## Credits

[Code Institute](https://codeinstitute.net/) - "Django Rest" learning materials followed during the initial set-up of this project, installing dependencies, setting up user registration and authentication, setting up pagination and deploying to Heroku.

### Specific code

The following code from [Code Institute's](https://codeinstitute.net/) Django rest module has been copied and reused within this project:

- validate_image method found in the FocusSerializer

### Images

[Code Institute](https://codeinstitute.net/) - The default post image from the "Django Rest" walkthrough has been used here as the default focus image.

[Return to contents list](#contents)

## Acknowledgements

[Code Institute](https://codeinstitute.net/) - The majority of the coding skills, knowledge and understanding showcased in this project have been learnt through the 'Diploma of Full stack software development' that I am completing with Code Institute.

Django Rest Framework documentation was used throughout the building of this project, in particular to support with:

- [Permissions](https://www.django-rest-framework.org/api-guide/permissions/#permissions) including setting a default permission class and writing a custom permission.
- [Querysets](https://www.django-rest-framework.org/api-guide/viewsets/#modelviewset) and controlling what is being pulled from the database as part of a view.
- [Filtering](https://www.django-rest-framework.org/api-guide/filtering/#filtering) including ordering and filtering.
- [dj-rest-auth](https://dj-rest-auth.readthedocs.io/en/latest/configuration.html) and finding ways around bug #2.

[Return to contents list](#contents)
