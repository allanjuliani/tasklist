from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django.utils.translation import gettext as _

from tasklist.models import List, Task, Tag

admin.site.index_title = _('Home')
admin.site.site_header = _('Task List Administration')
admin.site.site_title = admin.site.site_header


@admin.register(List)
class ListAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'created')
    list_display_links = ('id',)
    list_filter = ('created',)
    list_per_page = 20
    search_fields = ('name',)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'count', 'created')
    list_display_links = ('id',)
    list_filter = ('created',)
    list_per_page = 20
    search_fields = ('name',)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    def list_link(self, obj):
        return format_html('<a href="{url}?id__exact={id}">{name}</a>',
                           url=reverse('admin:tasklist_list_changelist'),
                           id=obj.list_id,
                           name=obj.list.name)
    list_link.short_description = _('List')
    list_link.admin_order_field = 'list'

    autocomplete_fields = ('list', 'tags',)
    list_display = ('id', 'title', 'list_link', 'notes', 'priority', 'remind_me_on', 'activity_type', 'status',  'created',
                    'updated')
    list_display_links = ('id',)
    list_filter = ('priority', 'activity_type', 'status', 'tags', 'created', 'updated')
    list_per_page = 20
    search_fields = ('title',)

