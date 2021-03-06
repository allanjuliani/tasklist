from django import forms

from tasklist.models import List, Tag, Task


class ListForm(forms.ModelForm):
    class Meta:
        model = List
        widgets = {}
        fields = '__all__'


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        widgets = {}
        fields = (
            'id',
            'title',
            'list',
            'notes',
            'priority',
            'remind_me_on',
            'activity_type',
            'status',
            'tags',
        )


class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        widgets = {}
        exclude = ('count',)
        fields = ('name',)
