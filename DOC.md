## How to install

Is recommended to run the project:

- Ubuntu 18.08 or later
- Python 3.6 or later
- MySQL 5.6 or later or SQLite 3.24 or later

#### Ubuntu 18 Dependencies
`sudo apt-get install git python-virtualenv memcached libxml2-dev libxslt1-dev libevent-dev python-dev python3-dev libsasl2-dev libmysqlclient-dev libjpeg-dev libffi-dev libssl-dev -y` 

#### Ubuntu 20 Dependencies
`sudo apt-get install git python3-virtualenv memcached libxml2-dev libxslt1-dev libevent-dev python3-dev libsasl2-dev libmysqlclient-dev libjpeg-dev libffi-dev libssl-dev -y` 

#### Create the Virtualenv
`cd ~/ && virtualenv tasklist && mkdir tasklist/src && cd tasklist/src`

#### Clone the Project
`git clone git@bitbucket.org:allanjuliani/backend-challenge.git`

#### Activate Virtualenv
`source ~/tasklist/bin/activate`

#### Install Python Dependencies

`cd ~/tasklist/src/tasklist && pip install -r requirements.txt`

#### Install Database

Default is set SQLite. If you want to use MySQL, create the database:

```sql
OCREATE DATABASE tasklist CHARACTER SET utf8 COLLATE utf8_general_ci;
```

On settings.py, fill the default settings with your database configurations.  

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'tasklist.sqlite3',
    }
    # CREATE DATABASE tasklist CHARACTER SET utf8 COLLATE utf8_general_ci;
    # 'default': {
    #     'ENGINE': 'django.db.backends.mysql',
    #     'HOST': 'localhost',
    #     'NAME': 'tasklist',
    #     'USER': 'tasklist',
    #     'PASSWORD': '#S3nh4@Gr4nd3!N1ngu3m&Qu3br4.',
    #     'OPTIONS': {
    #         'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
    #     }
    # },
}
```
#### Run the migrations

`./manage.py migrate`

#### Create admin user

`./manage.py createsuperuser`

#### Create API Token to your user

`./manage.py drf_create_token [your user]`

#### Test the application

`./manage.py test`

or

`make test`

#### Running the application

`./manage.py runserver 0.0.0.0:8000` 

or, start in english

`make start` 

start in portuguese

`make start_br`

to stop

`make stop`

#### Logging
`tail -f tasklist.log`

#### Admin URL to access on browser
`http://localhost:8000/admin/`

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
