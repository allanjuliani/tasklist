import json
from json import JSONDecodeError

from django.http import JsonResponse
from django.utils.translation import gettext as _
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from tasklist.utils import (list_create, list_delete, list_list, list_update,
                            list_view, tag_create, tag_delete, tag_list,
                            tag_update, tag_view, task_create, task_delete,
                            task_list, task_update, task_view)


@api_view(['POST', 'GET'])
@permission_classes([IsAuthenticated])
def list_add_list(request):
    status = 406
    context = {}

    # POST - Add
    if request.method == 'POST':
        # Get Json from request body
        try:
            request_body = json.loads(request.body)

        # If Json is not valid
        except JSONDecodeError:
            context = {'detail': _('Invalid body format. Must be a valid Json')}

        # With a valid json
        else:
            # Get or create User, using Django Forms
            status, context = list_create(request_body)

    # GET - List
    elif request.method == 'GET':
        status, context = list_list()

    # Return json request
    return JsonResponse(context, safe=False, status=status)


@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
@permission_classes([IsAuthenticated])
def list_view_update_delete(request, list_id):
    status = 406
    context = {}

    # Delete list
    if request.method == 'DELETE':
        status, context = list_delete(list_id)

    # View list
    elif request.method == 'GET':
        status, context = list_view(list_id)

    # Update list
    elif request.method in ['PUT', 'PATCH']:
        # Get Json from request body
        try:
            request_body = json.loads(request.body)

        # If Json is not valid
        except json.JSONDecodeError:
            context = {'detail': _('Invalid body format. Must be a valid Json')}

        # With a valid json
        else:
            status, context = list_update(list_id, request_body)

    return JsonResponse(context, safe=False, status=status)


@api_view(['POST', 'GET'])
@permission_classes([IsAuthenticated])
def task_add_list(request):
    status = 406
    context = {}

    # POST - Add
    if request.method == 'POST':
        # Get Json from request body
        try:
            request_body = json.loads(request.body)

        # If Json is not valid
        except JSONDecodeError:
            context = {'detail': _('Invalid body format. Must be a valid Json')}

        # With a valid json
        else:
            # Get or create User, using Django Forms
            status, context = task_create(request_body)

    # GET - List
    elif request.method == 'GET':
        status, context = task_list()

    # Return json request
    return JsonResponse(context, safe=False, status=status)


@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
@permission_classes([IsAuthenticated])
def task_view_update_delete(request, task_id):
    status = 406
    context = {}

    # Delete task
    if request.method == 'DELETE':
        status, context = task_delete(task_id)

    # View task
    elif request.method == 'GET':
        status, context = task_view(task_id)

    # Update task
    elif request.method == 'PUT':
        # Get Json from request body
        try:
            request_body = json.loads(request.body)

        # If Json is not valid
        except json.JSONDecodeError:
            context = {'detail': _('Invalid body format. Must be a valid Json')}

        # With a valid json
        else:
            status, context = task_update(task_id, request_body)

    # Update task partial
    elif request.method == 'PATCH':
        # Get Json from request body
        try:
            request_body = json.loads(request.body)

        # If Json is not valid
        except json.JSONDecodeError:
            context = {'detail': _('Invalid body format. Must be a valid Json')}

        # With a valid json
        else:
            status, context = task_update(task_id, request_body, partial=True)

    return JsonResponse(context, safe=False, status=status)


@api_view(['POST', 'GET'])
@permission_classes([IsAuthenticated])
def tag_add_list(request):
    status = 406
    context = {}

    # POST - Add
    if request.method == 'POST':
        # Get Json from request body
        try:
            request_body = json.loads(request.body)

        # If Json is not valid
        except JSONDecodeError:
            context = {'detail': _('Invalid body format. Must be a valid Json')}

        # With a valid json
        else:
            # Get or create User, using Django Forms
            status, context = tag_create(request_body)

    # GET - List
    elif request.method == 'GET':
        status, context = tag_list()

    # Return json request
    return JsonResponse(context, safe=False, status=status)


@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
@permission_classes([IsAuthenticated])
def tag_view_update_delete(request, tag_id):
    status = 406
    context = {}

    # Delete list
    if request.method == 'DELETE':
        status, context = tag_delete(tag_id)

    # View list
    elif request.method == 'GET':
        status, context = tag_view(tag_id)

    # Update list
    elif request.method in ['PUT', 'PATCH']:
        # Get Json from request body
        try:
            request_body = json.loads(request.body)

        # If Json is not valid
        except json.JSONDecodeError:
            context = {'detail': _('Invalid body format. Must be a valid Json')}

        # With a valid json
        else:
            status, context = tag_update(tag_id, request_body)

    return JsonResponse(context, safe=False, status=status)
