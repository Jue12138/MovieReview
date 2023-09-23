# Movie Review

## Description

The Movie Review Web App is a platform designed to create a seamless experience for movie enthusiasts to share opinions and discover new films. It bridges the gap between large movie databases and community-driven content, offering a secure and convenient interface complete with Google Sign-In functionality.

## Features

1. Dynamic Movie Data Integration: Utilizes the OMDb API to provide real-time, comprehensive movie data, giving users accurate and up-to-date information.
2. User Registration & Authentication: Features a secure registration and login mechanism, enhanced by the option for users to authenticate using their existing Google credentials.
3. User Profiles: Offers personalized user profiles where users can set avatars and review their comment history.
4. Robust Backend: Engineered using Python and Flask, capitalizing on Flask's adaptability and simplicity to create a powerful backend.
5. Data Storage: Employs MongoDB for efficient, secure storage of user data, including registration details, avatars, and comments.
6. Security: Utilizes Flask-Login for session management, prioritizing user data security.
7. Structured Codebase: Implements Flask Blueprint to organize the application code, resulting in a more maintainable and scalable architecture.

## Technologies Used

1. Programming Language: Python
2. Web Framework: Flask
3. Database: MongoDB
4. Frontend: HTML, CSS, Jinja2
5. APIs: OMDb, Google OAuth
6. CI/CD: GitHub Actions

## Setup

To run this project, first set a virtual environment:
For Mac/Linux:

```bash
$ python3 -m venv venv        # creates environment
$ source ./venv/bin/activate  # enters environment
```

For Windows:

```bash
$ py -m venv venv             # creates environment
$ ./venv/Scripts/activate     # enters environment
```

Get in the environment, then you can clone this repo.
To install all necessary packages, run `pip3 install -r requirements.txt`
To run this project, in the project MovieReview directory and use the

```bash
export FLASK_APP=run.py
flask run
```

command.
