# Django tasklist

## Using Docker

### Install Docker

https://docs.docker.com/engine/install/

### Build project
```commandline
make build
```

### Start project
```commandline
make up
```

### Run tests
```commandline
make tests
```

### Create superuser for admin
```commandline
make createsuperuser
```

### Create token to rest api
```commandline
make createtoken username=[YOUR_USER]
```

#### Admin URL to access on browser
http://localhost/admin/

#### Remove
```commandline
make tasklist-remove
make tasklist-clean
```

### Without Docker

#### Ubuntu Dependencies
```commandline
sudo apt-get install git python-virtualenv memcached libxml2-dev libxslt1-dev libevent-dev python-dev python3-dev libsasl2-dev libmysqlclient-dev libjpeg-dev libffi-dev libssl-dev -y
```

#### Create the Virtualenv
```commandline
virtualenv venv
```

#### Activate Virtualenv
```commandline
source venv/bin/activate
```

#### Install Python Dependencies

```commandline
pip install -r requirements.txt
```

#### Install Database

```commandline
./manage.py migrate --settings=tasklist.settings_dev
```

#### Create admin user

```commandline
./manage.py createsuperuser --settings=tasklist.settings_dev
```

#### Create API Token to your user

```commandline
./manage.py drf_create_token [YOUR_USER] --settings=tasklist.settings_dev
```

#### Test the application

```commandline
./manage.py test --settings=tasklist.settings_dev
```

#### Running the application

```commandline
./manage.py runserver 0.0.0.0:8000 --settings=tasklist.settings_dev
```

#### Admin URL to access on browser
http://localhost:8000/admin/

## The REST API

#### Add List
- POST /api/list/
- Authorization: Token [TOKEN_GENERATED]
- Content-Type: application/json
```json
{
  "name": "List Name"
}
```

#### Show Lists
- GET /api/list/
- Authorization: Token [TOKEN_GENERATED]
- Content-Type: application/json

#### Load List
- GET /api/list/[list_id]/
- Authorization: Token [TOKEN_GENERATED]
- Content-Type: application/json

#### Edit List
PUT and PATCH are the same because there is just one field

- PUT /api/list/[list_id]/
- PATCH /api/list/[list_id]/
- Authorization: Token [TOKEN_GENERATED]
- Content-Type: application/json
```json
{
    "name": "The New Name"
}
```

#### Delete List
- DELETE /api/list/[list_id]/
- Authorization: Token [TOKEN_GENERATED]
- Content-Type: application/json

#### Add Tag
Important to add two tags!

- POST /api/tag/
- Authorization: Token [TOKEN_GENERATED]
- Content-Type: application/json
```json
{
  "name": "Tag A"
}
```

#### Show Tags
- GET /api/tag/
- Authorization: Token [TOKEN_GENERATED]
- Content-Type: application/json

#### Load Tag
- GET /api/tag/[list_id]/
- Authorization: Token [TOKEN_GENERATED]
- Content-Type: application/json

#### Edit Tag
PUT and PATCH are the same because there is just one field

- PUT /api/tag/[list_id]/
- PATCH /api/tag/[list_id]/
- Authorization: Token [TOKEN_GENERATED]
- Content-Type: application/json
```
{
    "name": "The New Name"
}

```

#### Delete Tag
- DELETE /api/tag/[tag_id]/
- Authorization: Token [TOKEN_GENERATED]
- Content-Type: application/json

#### Add Task
Fields:
```python
# Priority
LOW = 1
MEDIUM = 2
HIGH = 3

# Activity Type
INDOOR = 1
OUTDOOR = 2

# Status
OPEN = 1
DOING = 2
DONE = 3
```
- POST /api/task/
- Authorization: Token [TOKEN_GENERATED]
- Content-Type: application/json
```json
{
    "title": "Example Task",
    "list": 1,
    "notes": "This is an example",
    "priority": 1,
    "remind_me_on": "2020-09-09 01:01:01",
    "activity_type": 1,
    "status": 1,
    "tags": [1, 2]
}
```

#### Show Tasks
- GET /api/task/
- Authorization: Token [TOKEN_GENERATED]
- Content-Type: application/json

#### Load Tasks
- GET /api/task/[task_id]/
- Authorization: Token [TOKEN_GENERATED]
- Content-Type: application/json

#### Edit Task
- PUT /api/task/[task_id]/
- Authorization: Token [TOKEN_GENERATED]
- Content-Type: application/json
```json
{
    "title": "Example Edited",
    "list": 1,
    "notes": "This is an fully edited example",
    "priority": 3,
    "remind_me_on": "2020-09-10 13:00:00",
    "activity_type": 2,
    "status": 2,
    "tags": [1, 2]
}
```

#### Partial Edit Task
- PATCH /api/task/[task_id]/
- Authorization: Token [TOKEN_GENERATED]
- Content-Type: application/json
```json
{
    "title": "Works with any field",
    "status": 3
}
```

#### Delete Task
- DELETE /api/task/[task_id]/
- Authorization: Token [TOKEN_GENERATED]
- Content-Type: application/json
