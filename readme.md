# Run dev server
```
$ git clone https://github.com/AntonGorulev/MY-project.git
$ cd MY-project
$ python -m venv.venv
$ . .venv/bin/activate
$ pip install -r requirements.txt
$ python manage.py migrate
$ python manage.py runserver
```
## Application functionality:
### Creation, deletion, editing articles
#### Job description: unregistered user can only read articles
#### after registration, the user gets access to posting articles
#### posted articles can only be edited by the author
