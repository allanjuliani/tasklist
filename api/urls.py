from django.urls import path

from api.views import list_add_list, list_view_update_delete
from api.views import task_add_list, task_view_update_delete
from api.views import tag_add_list, tag_view_update_delete


urlpatterns = [
    path('list/', list_add_list, name='list-add-list'),
    path('list/<int:list_id>/', list_view_update_delete, name='list-view-update-delete'),
    path('task/', task_add_list, name='task-add-list'),
    path('task/<int:task_id>/', task_view_update_delete, name='task-view-update-delete'),
    path('tag/', tag_add_list, name='tag-add-list'),
    path('tag/<int:tag_id>/', tag_view_update_delete, name='tag-view-update-delete'),
]
