# Academic Adventure

ECM2434 - Group Software Engineering Project

### Group 19
___

The group members are:

1. Cameron Stackhouse
2. Simon Puttock
3. Leo Boekestein
4. Laison Kou
5. Mattis Nowell
6. Andrew Yau

This is a submission for Sprint 1. 
There are three types of document that you will find the following places.

## PROCESS DOCUMENTS
Our process documents are managed on Trello. The link to our project page is below. 
We have added both mattcollison2 and nr3391 to the board so it is visible for you to view.

Trello Page: [https://trello.com/b/LhVN7c3f/kanban]

We have also taken regular snapshots of our Kanban board to archive our progress. 
These are held in the repository below alongside meeting notes, agenda and minutes. 
These will be found in the repository below.

[./process-documents/](./process-documents/)


## TECHNICAL DOCUMENTS
Our technical documents are primarily managed on GitHub.

Github Repo: [https://github.com/cameronstackhouse/group-software-engineering]

We have also include the versioned source code for archiving.

[./technical-documents/](./technical-documents/)

## PRODUCT DOCUMENTS

Our product documents are available in the folder below.

[./product-documents/UI/](./product-documents/UI/)

## Introduction

Academic Adventure is a location-based RPG style browser game that allows students to meet 
others and explore their campus and city though location based events. Students are then 
rewarded for getting involved with stat changes and a virtual currency that they can spend 
on rewards.

By accessing a web app, users can confirm their attendance at events hosted by gamekeepers 
(lecturers or societies at the university). These events can be viewed via a map which also 
tracks the user’s location.


## Prerequisites, Installation, and Requirements

Python v3.9 was used for the development of this project.

The web app uses Django v4.0.1 which can be installed via pip install.

Django and all other requirements can be installed by running: 

pip install -r requirements.txt

## Getting Started

Currently Academic Adventure is designed to only work in Exeter, though we hope it will be
customizable by the end of the next sprint.

To run the server, simply run the command 'python manage.py runserver' in the mysite folder.
To access the site go to your host-address/academic_adventure.

To make a registered user into a gamemaster:

run 'python manage.py shell' and then enter the following commands.

from academic_adventure.models import CustomUser
user = CustomUser.objects.get(username="YourUser")
user.gamekeeper = True
user.save()

## Testing

To run tests for this project, run the following command within the mysite folder:

'python manage.py test academic_adventure'

## License

Copyright (c) 2022 ECM2434 Group 19

This program is free software: you can redistribute it and/or modify it under the terms of 
the GNU General Public License as published by the Free Software Foundation, either version 
3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; 
without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
