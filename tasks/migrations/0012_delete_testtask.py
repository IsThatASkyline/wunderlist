# Generated by Django 4.0.3 on 2022-09-05 14:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0011_alter_category_options_alter_tasks_user'),
    ]

    operations = [
        migrations.DeleteModel(
            name='TestTask',
        ),
    ]
