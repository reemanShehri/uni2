# Generated by Django 5.1.6 on 2025-04-25 09:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('firstapp', '0006_studentprofile_is_student'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='studentprofile',
            name='is_student',
        ),
    ]
