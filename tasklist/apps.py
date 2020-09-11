from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class TaskListConfig(AppConfig):
    name = 'tasklist'
    verbose_name = _('Task list')
