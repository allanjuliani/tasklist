# Generated by Django 3.1.1 on 2020-09-11 18:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='List',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True, verbose_name='Name')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
            ],
            options={
                'verbose_name': 'List',
                'verbose_name_plural': 'Lists',
                'db_table': 'list',
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True, verbose_name='Title')),
                ('count', models.IntegerField(default=0, verbose_name='Count')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
            ],
            options={
                'verbose_name': 'Tag',
                'verbose_name_plural': 'Tags',
                'db_table': 'tag',
            },
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=128, verbose_name='Title')),
                ('notes', models.CharField(max_length=255, verbose_name='Notes')),
                ('priority', models.SmallIntegerField(choices=[(1, 'Low'), (2, 'Medium'), (3, 'High')], db_index=True, default=2, verbose_name='Priority')),
                ('remind_me_on', models.DateTimeField(verbose_name='Remind me on')),
                ('activity_type', models.SmallIntegerField(choices=[(1, 'Indoor'), (2, 'Outdoor')], db_index=True, default=1, verbose_name='Activity Type')),
                ('status', models.SmallIntegerField(choices=[(1, 'Open'), (2, 'Doing'), (3, 'Done')], db_index=True, default=1, verbose_name='Status')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Updated')),
                ('list', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tasklist.list', verbose_name='List')),
                ('tags', models.ManyToManyField(to='tasklist.Tag')),
            ],
            options={
                'verbose_name': 'Task',
                'verbose_name_plural': 'Tasks',
                'db_table': 'task',
                'unique_together': {('list', 'title')},
            },
        ),
    ]
