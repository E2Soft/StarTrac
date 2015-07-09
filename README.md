# StarTrac
### A simple [django](https://www.djangoproject.com/) based task tracking system and repository browser.

## Dependencies:
- Django (1.7.1) https://www.djangoproject.com/
- GitPython (0.3.6) http://gitpython.readthedocs.org/en/stable/intro.html
```sh
$ pip install gitpython
```
- Git (1.7.0 or newer) http://git-scm.com/ (should be in PATH)
- Pillow (2.7.0) http://pillow.readthedocs.org/
```sh
$ pip install Pillow
```

## Deploy:
- install all dependencies
- pull StarTrac the project
- set GIT_REPO_PATH in src/StarTrac/settings.py to the path of your git repository (the dsefault value is "../.git" which tracks the projects own local git repository)
- for a quick start you can run a test server, in src/ do:
```sh
python manage.py migrate # to create a database
python manage.py createsuperuser # to create a django admin user
python manage.py runserver # to run the test server
```
- for other information on how to deploy a django project see the official [documentation](https://docs.djangoproject.com)
	
## Features:
- Tasks tracking.
- Milestones tracking.
- Requirements tracking.
- Kanban table: The tasks are organized in 4 sections 'Created', 'On Wait', 'Accepted' and 'Closed' and displayed in a table on the home page. Drag and drop the tasks to change their state.
- Project time line showing important events in the project.
- Git repository browsing and code comparison.
- Graphic reports.

## Licence:
Licensed under MIT license.