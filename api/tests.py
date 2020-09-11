import pytz

from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.datetime_safe import datetime
from django.utils.timezone import make_aware
from django.utils.translation import gettext as _

from tasklist.models import List, Task, Tag


class ApiTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        print('\n== API Test Case ==')

    def setUp(self):
        # Create admin user
        user = User.objects.create(username='tester', is_superuser=True, is_staff=True)

        # Crate token for every test
        self.token, created = Token.objects.get_or_create(user=user)

        # Create list base for list, view, update and delete test
        data = {'name': 'List Base'}
        self.list_base = List.objects.create(**data)

        # Create Tag base for list, view, update and delete test
        data = {'name': 'Tag A'}
        self.tag_base = Tag.objects.create(**data)

        # Create Task base for list, view, update and delete test
        data = {
            'title': 'Example Task',
            'list_id': 1,
            'notes': 'This is an example',
            'priority': 1,
            'remind_me_on': make_aware(datetime(2020, 9, 15, 13, 0, 0)),
            'activity_type': 1,
            'status': 1,
        }
        self.task_base = Task.objects.create(**data)
        self.task_base.tags.add(self.tag_base)

    """
    List Tests
    """
    def test_list_add(self):
        """
        POST /api/list/
        data {'name': 'List Name'}
        response 200 {'message': 'New list created', 'data': {'list_id': 2}}
        """
        print("\nTest List add")

        url = reverse('list-add-list')
        data = {'name': 'List Name'}
        response = self.client.post(url, data, HTTP_AUTHORIZATION=f'Token {self.token}', format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {'message': 'New list created', 'data': {'list_id': 2}})

    def test_list_list(self):
        """
        GET /api/list/
        response 200 [{'id': 1, name': 'List Base', 'created': '2020-09-11T14:31:25.347Z'}]
        """
        print("\nTest List list")

        url = reverse('list-add-list')
        response = self.client.get(url, HTTP_AUTHORIZATION=f'Token {self.token}', format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 1)

    def test_list_load(self):
        """
        GET /api/list/1/
        response 200 {'id': 1, name': 'List Base'}
        """
        print("\nTest List load")

        url = reverse('list-view-update-delete', args=(self.list_base.id,))
        response = self.client.get(url, HTTP_AUTHORIZATION=f'Token {self.token}')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {
            'id': self.list_base.id,
            'name': self.list_base.name,
            'created': f"{self.list_base.created.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3]}Z"
        })

    def test_list_full_update(self):
        """
        PUT /api/list/1/
        data data {'name': 'New list name fully updated'}
        response 200 {'detail': 'List 1 updated', 'data': {
            'id': 1,
            'name': 'New list name fully updated',
            'created': '2020-09-11T00:03:10.788Z'}}
        """
        print("\nTest List full update")

        url = reverse('list-view-update-delete', args=(self.list_base.id,))
        data = {'name': 'New list name fully updated'}
        response = self.client.put(url, data, HTTP_AUTHORIZATION=f'Token {self.token}', format='json')

        list_id = self.list_base.id

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {'detail': _(f'List {list_id} updated'), 'data': {
            'id': self.list_base.id,
            'name': data.get('name'),
            'created': f"{datetime.strftime(self.list_base.created, '%Y-%m-%dT%H:%M:%S.%f')[:-3]}Z"
        }})

    def test_list_partial_update(self):
        """
        PATCH /api/list/1/
        data {'name': 'New list name partial updated'}
        response 200 {'detail': 'List 1 updated', 'data': {
            'id': 1,
            'name': 'New list name partial updated',
            'created': '2020-09-11T00:03:10.788Z'}}
        """
        print("\nTest List partial update")

        url = reverse('list-view-update-delete', args=(self.list_base.id,))
        data = {'name': 'New list name partial updated'}
        response = self.client.patch(url, data, HTTP_AUTHORIZATION=f'Token {self.token}', format='json')

        list_id = self.list_base.id

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {'detail': _(f'List {list_id} updated'), 'data': {
            'id': self.list_base.id,
            'name': data.get('name'),
            'created': f"{datetime.strftime(self.list_base.created, '%Y-%m-%dT%H:%M:%S.%f')[:-3]}Z"
        }})

    def test_list_delete(self):
        """
        DELETE /api/list/1/
        response {'message': 'List 1 deleted'}
        """
        print("\nTest List delete")

        url = reverse('list-view-update-delete', args=(self.list_base.id,))
        response = self.client.delete(url, HTTP_AUTHORIZATION=f'Token {self.token}')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {'detail': f'List {self.list_base.id} deleted'})

    """
    Tag Tests
    """
    def test_tag_add(self):
        """
        POST /api/tag/
        data {'name': 'Tag Name'}
        response 200 {'message': 'New tag created', 'data': {'tag_id': 2}}
        """
        print("\nTest Tag add")

        url = reverse('tag-add-list')
        data = {'name': 'Tag Name'}
        response = self.client.post(url, data, HTTP_AUTHORIZATION=f'Token {self.token}', format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {'message': 'New Tag created', 'data': {'tag_id': 2}})

    def test_tag_list(self):
        """
        GET /api/tag/
        response 200 [{'id': 1, name': 'Tag Base', 'created': '2020-09-11T14:31:25.347Z'}]
        """
        print("\nTest Tag list")

        url = reverse('tag-add-list')
        response = self.client.get(url, HTTP_AUTHORIZATION=f'Token {self.token}', format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 1)

    def test_tag_load(self):
        """
        GET /api/tag/1/
        response 200 {'id': 1, 'name': 'Tag A', 'count': 1, 'created': '2020-09-11T17:27:50.086Z'}
        """
        print("\nTest Tag load")
        url = reverse('tag-view-update-delete', args=(self.tag_base.id,))
        response = self.client.get(url, HTTP_AUTHORIZATION=f'Token {self.token}')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {
            'id': self.tag_base.id,
            'count': Task.objects.filter(tags=self.tag_base).count(),
            'name': self.tag_base.name,
            'created': f"{self.tag_base.created.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3]}Z"
        })

    def test_tag_full_update(self):
        """
        PUT /api/tag/1/
        data data {'name': 'New list name fully updated'}
        response 200 {'detail': 'Tag 1 updated', 'data': {
            'id': 1,
            'name': 'New list name fully updated',
            'count': 1,
            'created': '2020-09-11T00:03:10.788Z'}}
        """
        print("\nTest Tag full update")

        url = reverse('tag-view-update-delete', args=(self.tag_base.id,))
        data = {'name': 'New list name fully updated'}
        response = self.client.put(url, data, HTTP_AUTHORIZATION=f'Token {self.token}', format='json')

        tag_id = self.tag_base.id

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {'detail': _(f'Tag {tag_id} updated'), 'data': {
            'id': self.tag_base.id,
            'name': data.get('name'),
            'count': Task.objects.filter(tags=self.tag_base).count(),
            'created': f"{datetime.strftime(self.tag_base.created, '%Y-%m-%dT%H:%M:%S.%f')[:-3]}Z"
        }})

    def test_tag_partial_update(self):
        """
        PATCH /api/tag/1/
        data {'name': 'New list name partial updated'}
        response 200 {'detail': 'Tag 1 updated', 'data': {
            'id': 1,
            'name': 'New list name partial updated',
            'count': 1,
            'created': '2020-09-11T00:03:10.788Z'}}
        """
        print("\nTest Tag partial update")

        url = reverse('tag-view-update-delete', args=(self.tag_base.id,))
        data = {'name': 'New list name partial updated'}
        response = self.client.patch(url, data, HTTP_AUTHORIZATION=f'Token {self.token}', format='json')

        tag_id = self.tag_base.id

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {'detail': _(f'Tag {tag_id} updated'), 'data': {
            'id': self.tag_base.id,
            'name': data.get('name'),
            'count': Task.objects.filter(tags=self.tag_base).count(),
            'created': f"{datetime.strftime(self.tag_base.created, '%Y-%m-%dT%H:%M:%S.%f')[:-3]}Z"
        }})

    def test_tag_delete(self):
        """
        DELETE /api/tag/1/
        response {'message': 'Tag 1 deleted'}
        """
        print("\nTest Tag delete")

        url = reverse('tag-view-update-delete', args=(self.tag_base.id,))
        response = self.client.delete(url, HTTP_AUTHORIZATION=f'Token {self.token}')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {'detail': f'Tag {self.tag_base.id} deleted'})

    """
    Task Tests
    """
    def test_task_add(self):
        """
        POST /api/task/
        data {
            'title': 'Example',
            'list': 1,
            'notes': 'This is an example',
            'priority': 1,
            'remind_me_on': '2020-09-09 01:01:01',
            'activity_type': 1,
            'status': 1
            'tags': [1]
        }
        response 200 {'message': 'New task created', 'data': {'task_id': 2}}
        """
        print("\nTest Task add")

        url = reverse('task-add-list')
        data = {
            'title': 'Example',
            'list': 1,
            'notes': 'This is an example',
            'priority': 1,
            'remind_me_on': make_aware(datetime(2020, 9, 15, 13, 0, 0)),
            'activity_type': 1,
            'status': 1,
            'tags': [1]
        }
        response = self.client.post(url, data, HTTP_AUTHORIZATION=f'Token {self.token}', format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {'message': 'New task created', 'data': {'task_id': 2}})

    def test_task_list(self):
        """
        GET /api/task/
        response 200 [{'id': 1, name': 'List Base', 'created': '2020-09-11T14:31:25.347Z'}]
        """
        print("\nTest Task list")

        url = reverse('task-add-list')
        response = self.client.get(url, HTTP_AUTHORIZATION=f'Token {self.token}', format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 1)

    def test_task_load(self):
        """
        GET /api/task/1/
        response 200 {
            'id': 1,
            'list_id': 1,
            'list': 'List Base',
            'title': 'Example Task',
            'notes': 'This is an example',
            'priority_id': 1,
            'priority': 'Low',
            'remind_me_on': '2020-09-15 13:00:00',
            'activity_type_id': 1, 'activity_type':
            'Indoor', 'status_id': 1,
            'status': 'Open',
            'created': '2020-09-11 12:34:57',
            'updated': '2020-09-11 12:34:57',
            'tags': [{'id': 1, 'name': 'Tag A', 'created': '2020-09-11T17:27:50.086Z'}]}
        """
        print("\nTest Task load")

        url = reverse('task-view-update-delete', args=(self.task_base.id,))
        response = self.client.get(url, HTTP_AUTHORIZATION=f'Token {self.token}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {
            'id': self.task_base.id,
            'list_id': self.task_base.list_id,
            'list': self.task_base.list.name,
            'title': self.task_base.title,
            'notes': self.task_base.notes,
            'priority_id': self.task_base.priority,
            'priority': self.task_base.get_priority_display(),
            'remind_me_on': self.task_base.remind_me_on.strftime('%Y-%m-%d %H:%M:%S'),
            'activity_type_id': self.task_base.activity_type,
            'activity_type': self.task_base.get_activity_type_display(),
            'status_id': self.task_base.status,
            'status': self.task_base.get_status_display(),
            'created': self.task_base.created.astimezone().strftime('%Y-%m-%d %H:%M:%S'),
            'updated': self.task_base.created.astimezone().strftime('%Y-%m-%d %H:%M:%S'),
            'tags': [{
                'id': self.tag_base.id,
                'name': self.tag_base.name,
                'count': Task.objects.filter(tags=self.tag_base).count(),
                'created': f"{self.tag_base.created.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3]}Z"}]})

    def test_task_full_update(self):
        """
        PUT /api/task/1/
        data {'name': 'New task name fully updated'}
        response 200 {'detail': 'Task 1 updated', 'data': {{
            'title': 'Example Edited',
            'list': 5,
            'notes': 'This is an fully edited example',
            'priority': 3,
            'remind_me_on': '2020-09-10 13:00:00',
            'activity_type': 2,
            'status': 2,
            'tags': [{'id': 1, 'name': 'Tag A', 'created': '2020-09-11T17:27:50.086Z'}]}
        """
        print("\nTest Task full update")

        url = reverse('task-view-update-delete', args=(self.task_base.id,))
        data = {
            'title': 'Example Edited',
            'list': 1,
            'notes': 'This is an fully edited example',
            'priority': 3,
            'remind_me_on': make_aware(datetime(2020, 9, 15, 13, 0, 0)),
            'activity_type': 2,
            'status': 2,
            'tags': [1]}
        response = self.client.put(url, data, HTTP_AUTHORIZATION=f'Token {self.token}', format='json')

        task_id = self.task_base.id
        tz = pytz.timezone('UTC')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {'detail': _(f'Task {task_id} updated'), 'data': {
            'id': self.task_base.id,
            'list_id': data.get('list'),
            'title': data.get('title'),
            'notes': data.get('notes'),
            'priority': data.get('priority'),
            'remind_me_on': f"{self.task_base.remind_me_on.astimezone(tz).strftime('%Y-%m-%dT%H:%M:%S.%f')[:-7]}Z",
            'activity_type': data.get('activity_type'),
            'status': data.get('status'),
            'created': f"{(self.task_base.created.strftime('%Y-%m-%dT%H:%M:%S.%f'))[:-3]}Z",
            'updated': response.json().get('data').get('updated'),
        }})

    def test_task_partial_update(self):
        """
        PATCH /api/task/1/
        data {'title': 'Works with any field', 'status': 3}
        response 200 {'detail': 'Task 1 updated', 'data': {
            'id': 1,
            'list_id': 1,
            'title': 'Works with any field',
            'notes': 'This is an example',
            'priority': 1,
            'remind_me_on': '2020-09-15T16:00:00Z',
            'activity_type': 1, 'status': 3,
            'created': '2020-09-11T16:29:03.741Z',
            'updated': '2020-09-11T16:29:03.746Z'}}
        """
        print("\nTest Task partial update")

        url = reverse('task-view-update-delete', args=(self.task_base.id,))
        data = {'title': 'Works with any field', 'status': 3}
        response = self.client.patch(url, data, HTTP_AUTHORIZATION=f'Token {self.token}', format='json')

        task_id = self.task_base.id
        tz = pytz.timezone('UTC')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {'detail': _(f'Task {task_id} updated'), 'data': {
            'id': self.task_base.id,
            'list_id': self.task_base.list_id,
            'title': data.get('title'),
            'notes': self.task_base.notes,
            'priority': self.task_base.priority,
            'remind_me_on': f"{self.task_base.remind_me_on.astimezone(tz).strftime('%Y-%m-%dT%H:%M:%S.%f')[:-7]}Z",
            'activity_type': self.task_base.activity_type,
            'status': data.get('status'),
            'created': f"{(self.task_base.created.strftime('%Y-%m-%dT%H:%M:%S.%f'))[:-3]}Z",
            'updated': response.json().get('data').get('updated'),
        }})

    def test_task_delete(self):
        """
        DELETE /api/task/1/
        response {'message': 'List 1 deleted'}
        """
        print("\nTest Task delete")

        url = reverse('task-view-update-delete', args=(self.task_base.id,))
        response = self.client.delete(url, HTTP_AUTHORIZATION=f'Token {self.token}')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {'detail': f'Task {self.task_base.id} deleted'})