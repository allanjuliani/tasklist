from django.utils.translation import gettext as _

from tasklist.forms import ListForm, TaskForm, TagForm
from tasklist.models import List, Task, Tag


def list_create(request_body):
    list_form = ListForm(request_body)

    # If the form is valid
    if list_form.is_valid():
        # Save list
        _list = list_form.save()
        # return new user id
        return 200, {'message': _('New list created'), 'data': {'list_id': _list.id}}

    # If there is any form error, return it
    else:
        return 406, {'data': list_form.errors.as_json()}


def list_list():
    # Get the query set as dick and insert into a list
    context = [entry for entry in List.objects.values()]
    return 200, context


def list_delete(list_id):
    # Load list
    _list = List.objects.filter(id=list_id)

    if _list.exists():
        # Delete list and task related
        _list.delete()

        return 200, {'detail': _(f'List {list_id} deleted')}

    else:
        return 404, {'detail': _('List not found')}


def list_view(list_id):
    # Load list
    _list = List.objects.values().filter(id=list_id).first()

    if _list:
        return 200, _list
    else:
        return 404, {'detail': _('List not found')}


def list_update(list_id, request_body):
    # Load list
    _list = List.objects.filter(id=list_id).first()

    # If find the list
    if _list:
        # Call form
        list_form = ListForm(request_body, instance=_list)

        # If the form is valid
        if list_form.is_valid():
            list_form.save()

            # Load data to print at the return
            data = List.objects.values().get(id=list_id)
            return 200, {'detail': _(f'List {list_id} updated'), 'data': data}

        # If there is and error, return it
        else:
            return 406, {'data': list_form.errors.as_json()}

    # Not found any list
    else:
        return 404, {'error': _('List not found')}


def tag_create(request_body):
    tag_form = TagForm(request_body)

    # If the form is valid
    if tag_form.is_valid():
        # Save list
        _list = tag_form.save()
        # return new user id
        return 200, {'message': _('New Tag created'), 'data': {'tag_id': _list.id}}

    # If there is any form error, return it
    else:
        return 406, {'data': tag_form.errors.as_json()}


def tag_list():
    # Get the query set as dick and insert into a list
    context = [entry for entry in Tag.objects.values()]
    return 200, context


def tag_delete(tag_id):
    # Load tag
    tag = Tag.objects.filter(id=tag_id)

    if tag.exists():
        # Delete tag and task related
        tag.delete()

        return 200, {'detail': _(f'Tag {tag_id} deleted')}

    else:
        return 404, {'detail': _('Tag not found')}


def tag_view(tag_id):
    # Load tag
    tag = Tag.objects.values().filter(id=tag_id).first()

    if tag:
        return 200, tag
    else:
        return 404, {'detail': _('Tag not found')}


def tag_update(tag_id, request_body):
    # Load tag
    tag = Tag.objects.filter(id=tag_id).first()

    # If find the tag
    if tag:
        # Call form
        tag_form = TagForm(request_body, instance=tag)

        # If the form is valid
        if tag_form.is_valid():
            tag_form.save()

            # Load data to print at the return
            data = Tag.objects.values().get(id=tag_id)
            return 200, {'detail': _(f'Tag {tag_id} updated'), 'data': data}

        # If there is and error, return it
        else:
            return 406, {'data': tag_form.errors.as_json()}

    # Not found any tag
    else:
        return 404, {'error': _('Tag not found')}


def task_create(request_body):
    task_form = TaskForm(request_body)

    # If the form is valid
    if task_form.is_valid():
        # Save task
        task = task_form.save()
        # return new user id
        return 200, {'message': _('New task created'), 'data': {'task_id': task.id}}

    # If there is any form error, return it
    else:
        return 406, {'data': task_form.errors.as_json()}


def task_list():
    # Get the query set as dick and insert into a list
    context = []
    for task in Task.objects.select_related('list').all():
        context.append({
            'id': task.id,
            'list_id': task.list_id,
            'list': task.list.name,
            'title': task.title,
            'notes': task.notes,
            'priority_id': task.priority,
            'priority': task.get_priority_display(),
            'remind_me_on': task.remind_me_on,
            'activity_type_id': task.activity_type,
            'activity_type': task.get_activity_type_display(),
            'status_id': task.status,
            'status': task.get_status_display(),
            'created': task.created.strftime('%Y-%m-%d %H:%M:%S'),
            'updated': task.updated,
            'tags': [entry for entry in task.tags.values()]
        })
    return 200, context


def task_delete(task_id):
    # Load task
    task = Task.objects.filter(id=task_id)

    if task.exists():
        # Delete task and task related
        task.delete()

        return 200, {'detail': _(f'Task {task_id} deleted')}

    else:
        return 404, {'detail': _('Task not found')}


def task_view(task_id):
    # Load task
    task = Task.objects.filter(id=task_id).first()

    if task:
        return 200, {
            'id': task.id,
            'list_id': task.list_id,
            'list': task.list.name,
            'title': task.title,
            'notes': task.notes,
            'priority_id': task.priority,
            'priority': task.get_priority_display(),
            'remind_me_on': task.remind_me_on.astimezone().strftime('%Y-%m-%d %H:%M:%S'),
            'activity_type_id': task.activity_type,
            'activity_type': task.get_activity_type_display(),
            'status_id': task.status,
            'status': task.get_status_display(),
            'created': task.created.astimezone().strftime('%Y-%m-%d %H:%M:%S'),
            'updated': task.updated.astimezone().strftime('%Y-%m-%d %H:%M:%S'),
            'tags': [entry for entry in task.tags.values()]
        }
    else:
        return 404, {'detail': _('Task not found')}


def task_update(task_id, request_body, partial=False):
    # Load task
    task = Task.objects.select_related('list').filter(id=task_id).first()

    # If find the task
    if task:
        # If is partial, create a new list with task dict
        if partial:
            task_dict = task.__dict__
            # update the new list with data sent
            for key in request_body:
                task_dict[key] = request_body.get(key)

            # Add list because on dict is list_id
            task_dict.update({'list': task_dict.get('list_id')})
            task_dict.update({'tags': [entry.id for entry in task.tags.all()]})

            # Call TaskForm with new list
            task_form = TaskForm(task_dict, instance=task)
        else:
            # Call normal form
            task_form = TaskForm(request_body, instance=task)

        # If the form is valid
        if task_form.is_valid():
            task_form.save()

            # Load data to print at the return
            data = Task.objects.values().get(id=task_id)
            return 200, {'detail': _(f'Task {task_id} updated'), 'data': data}

        # If there is and error, return it
        else:
            return 406, {'data': task_form.errors.as_json()}

    # Not found any task
    else:
        return 404, {'error': _('Task not found')}
