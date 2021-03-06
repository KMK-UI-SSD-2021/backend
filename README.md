[![Codacy Badge](https://app.codacy.com/project/badge/Grade/31c3908646524e9f83706f92dd1b5b68)](https://www.codacy.com/gh/KMK-UI-SSD-2021/backend/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=KMK-UI-SSD-2021/backend&amp;utm_campaign=Badge_Grade)
[![codecov](https://codecov.io/gh/KMK-UI-SSD-2021/backend/branch/master/graph/badge.svg?token=F4EG13WIQK)](https://codecov.io/gh/KMK-UI-SSD-2021/backend)

# KMK Backend

This repository contains the backend part of the KMK project


# Demo
### [Watch it on Youtube](https://youtu.be/UVgbwiAolcU)


# Getting started


### Pre-commit hooks
After you cloned the repository, make sure that you have pre-commit package installed. To install it globally run the following code
```
$ pip3 install pre-commit==2.13.0
```
Then, to setup pre-commit hooks run this code in the root of the working directory
```
$ pre-commit install
```


### Running locally
To run the project on your local machine simply execute the following code
```
$ docker-compose up --build
```
Then, you can see the API documentation on http://127.0.0.1:5000/docs

### Testing
To run the tests execute the following code
```
$ scripts/run_tests.sh
```


# Requirements

### Stakeholder's Roles


| Stakeholder | Roles | Responsibilities |
| -------- | -------- | -------- |
| Alexander Kurmazov     | Backend developer     | Implement the REST API <br /> Implement the backend business logic <br /> Write unit test <br /> Setup Github Actions <br /> Deploy solution on a remote machine <br /> Prepare deliverables and artifacts |
| Daniil Gubaydullin | Frontend developer | Design a low fidelity prototype <br /> Implement an integration with the API <br /> Layout a web-page |
| Nurdaulet Kunkhozhaev | Frontend developer | Design a low fidelity prototype <br /> Layout a web-page |
| Valentin Chernyshov | Project Manager | Conduct status meeting with the team <br /> Setup Jira workflow |

### [RUP Deliverable](https://docs.google.com/document/d/1UwLZRrJ5waXoj0tItV4rKKHDpgBjYpTk/edit?usp=sharing&ouid=114466313595428679485&rtpof=true&sd=true)



# Design
In this project, we follow the design patterns of Domain Driven Development. The domains are *User*, *Lobby*, and *Statistics*; on top of them, there are three corresponding repositories that are responsible for interacting with the DB. The API, in turn, uses services that proxy the interaction between the Fast API client and repositories.

![](https://i.imgur.com/8CBc9XZ.png)


# Architecture

### Abstract
The architecture of the project is typical for a web application. In the middle, there is a RESTful API backend, that can be used by different clients: i.g., a web client, a telegram bot, Postman, etc.

The interaction with a third-party image hosting service is prototyped. Although, it can can be implemented on a client, since the backend accepts images in form of urls for them.

![](https://i.imgur.com/DgSTCO5.png)


### Static View
![](https://i.imgur.com/1oY5y87.png)


### Dynamic View
![](https://i.imgur.com/8GRtcPh.png)


# Code linters and Tests

### Pre-commit hooks
Before commiting the changes we've made, it is always beneficial to double-check whether there are any issues in the new code, so we use *isort* and *flake8* checkers for this purpose.

For example, a pre-commit report might look like this


![](https://i.imgur.com/e5yqTLt.png)


### Linters
Linting is the first stage of the Github Actions CI pipeline in this repository. The same linters, *isort* and *flake8*, are used to check the quality of the last pushed code to a branch.


![](https://i.imgur.com/RVvwlpU.png)

After the pipeline is finished, the report is uploaded to *Codacy*, which yields code quality dashboards about our repository


![](https://i.imgur.com/rRuNra4.png)


### Coverage
Tests are ran whenever new code is pushed to the remote; they help us to ensure that the code works as intended, and that no new bugs appeared in our codebase.


![](https://i.imgur.com/vA5c2HH.png)


After the pipeline is finished, the coverage report is uploaded to *codecov*, where a developer may find the visuals on tests coverage in the repository.


![](https://i.imgur.com/Dt51Cvf.png)


Also, the *Codecov Bot* assists with coverage information when a Pull Request is reviewed


![](https://i.imgur.com/bDiTT2L.png)
