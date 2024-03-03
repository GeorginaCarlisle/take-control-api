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

## Frameworks and Libraries

[Return to contents list](#contents)

## Tools and Technologies

[Return to contents list](#contents)

## Testing and Validation

See [TESTING.md](TESTING.md) for all testing and validation.

[Return to contents list](#contents)

## Bugs and Fixes

[Return to contents list](#contents)

## Deployment

[Return to contents list](#contents)

## Cloning this repository

[Return to contents list](#contents)

## Forking a branch

[Return to contents list](#contents)

## Credits

[Return to contents list](#contents)

## Acknowledgements

[Return to contents list](#contents)
