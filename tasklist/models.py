from django.db import models
from django.dispatch import receiver
from django.utils.translation import gettext as _


class List(models.Model):
    name = models.CharField(_('Name'), max_length=255, unique=True)
    created = models.DateTimeField(_('Created'), auto_now_add=True)

    class Meta:
        db_table = 'list'
        verbose_name = _('List')
        verbose_name_plural = _('Lists')

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(_('Title'), max_length=255, unique=True)
    count = models.IntegerField(_('Count'), default=0)
    created = models.DateTimeField(_('Created'), auto_now_add=True)

    class Meta:
        db_table = 'tag'
        verbose_name = _('Tag')
        verbose_name_plural = _('Tags')

    def __str__(self):
        return self.name


class Task(models.Model):
    """
    The fields activity_type and status was supposed to be string, but since it's always the same value, I think it's
    better to be small integer fields with Django Choices.
    I also think that in a real system, would be necessary to set a index for these fields, in case we have Reports.
    """

    class Priority(models.IntegerChoices):
        LOW = 1, _('Low')
        MEDIUM = 2, _('Medium')
        HIGH = 3, _('High')

    class ActivityType(models.IntegerChoices):
        INDOOR = 1, _('Indoor')
        OUTDOOR = 2, _('Outdoor')

    class Status(models.IntegerChoices):
        OPEN = 1, _('Open')
        DOING = 2, _('Doing')
        DONE = 3, _('Done')

    list = models.ForeignKey(List, verbose_name=_('List'), on_delete=models.CASCADE)
    title = models.CharField(_('Title'), max_length=128)
    notes = models.CharField(_('Notes'), max_length=255)
    priority = models.SmallIntegerField(
        _('Priority'), choices=Priority.choices, default=Priority.MEDIUM, db_index=True
    )
    remind_me_on = models.DateTimeField(_('Remind me on'))
    activity_type = models.SmallIntegerField(
        _('Activity Type'),
        choices=ActivityType.choices,
        default=ActivityType.INDOOR,
        db_index=True,
    )
    status = models.SmallIntegerField(
        _('Status'), choices=Status.choices, default=Status.OPEN, db_index=True
    )
    tags = models.ManyToManyField(Tag)
    created = models.DateTimeField(_('Created'), auto_now_add=True)
    updated = models.DateTimeField(_('Updated'), auto_now=True)

    class Meta:
        """
        Unique together just allow create same Task name for different List
        """

        unique_together = (('list', 'title'),)
        db_table = 'task'
        verbose_name = _('Task')
        verbose_name_plural = _('Tasks')

    def __str__(self):
        return self.title


@receiver(models.signals.m2m_changed, sender=Task.tags.through)
def change_users(signal, sender, instance, action, pk_set, **kwargs):
    """
    Save total tags per task, using signal after change tags many to many
    """
    tags = instance.tags.all()
    for tag in tags:
        if action == 'pre_remove':
            tag.count = Task.objects.filter(tags=tag).count() - 1
        else:
            tag.count = Task.objects.filter(tags=tag).count()
        tag.save(update_fields=['count'])
