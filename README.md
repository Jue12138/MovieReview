# Movie Review

## Description

The Movie Review Web App provides a seamless experience for movie enthusiasts to share their opinions and explore others. By fusing modern technologies and focusing on user-centric design, the app bridges the gap between movie databases and community-driven content. With integrated Google sign-ins and secure data storage, the platform is both secure and convenient for its users.

## Features

1. Dynamic Movie Data Integration: Incorporated the OMDb API to fetch detailed movie data, ensuring users always have access to up-to-date movie information.
2. User Registration & Authentication: Implemented a secure registration and login system, allowing users to create personal accounts. Added the option for users to log in using their Google credentials, making the process more streamlined and user-friendly.
3. User Profiles: Users have the ability to set avatars and view their comment history, offering a personalized experience.
   Robust Backend: The app's backend was architected using Python and Flask, capitalizing on Flask's flexibility and ease of use.
4. Data Storage: Leveraged MongoDB as a database, ensuring the efficient storage and retrieval of user-specific data including registration details, avatars, and comments.
5. Security: Prioritized user data security by integrating Flask-Login, ensuring secure user sessions.
6. Structured Codebase: Utilized Flask Blueprint framework to organize the codebase, resulting in an easily maintainable and scalable application structure.

## Technologies Used

Programming Language: Python
Web Framework: Flask
Database: MongoDB
Frontend: HTML, CSS, Jinja2
APIs: OMDb, Google OAuth

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
