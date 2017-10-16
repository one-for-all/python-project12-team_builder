## Web app for organizing group project

### Instructions for setting up the project
1. Create python3 virtual environment
2. Activate the virtual environment
3. Install packages using requirements.txt
4. Change directory into team_builder
5. python manage.py migrate
6. python scripts/data_import.py
7. Start a local email server for testing: python -m smtpd -n -c
DebuggingServer localhost:1025

Now, all set, run the project as usual by: python manage.py runserver

### Notes:
1. Notification on application status appears on the terminal with local email
 server
2. All fields for project creation are required