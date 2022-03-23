# Academic Adventure

ECM2434 - Group Software Engineering Project

### Group 19
___

The group members are:

- Cameron Stackhouse
- Simon Puttock
- Leo Boekestein
- Laison Kou
- Mattis Nowell
- Andrew Yau

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

Currently Academic Adventure is designed to only work in Exeter. 

To run the server, simply run the command 'python manage.py runserver' in the mysite folder.
To access the site go to your host-address/academic-adventure.

To make a registered user into a gamekeeper:

As a superuser access /admin at the URL and do the following:
- Go to the account you want to make a gamekeeper in Users
- Scroll to the bottom of the page and tick the gamekeeper option
- Click save

OR

run 'python manage.py shell' and then enter the following commands.

- from academic_adventure.models import CustomUser
- user = CustomUser.objects.get(username="YourUser")
- user.gamekeeper = True
- user.save()

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

For more information please see the attached LICENCE file or visit: https://www.gnu.org/licenses
