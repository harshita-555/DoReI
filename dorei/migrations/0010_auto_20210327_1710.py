# Generated by Django 3.1.7 on 2021-03-27 17:10

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dorei', '0009_auto_20210327_1604'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='manager',
            name='mobile_number',
        ),
        migrations.AddField(
            model_name='manager',
            name='phone',
            field=models.CharField(blank=True, max_length=15, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.", regex='^\\+?1?\\d{9,15}$')]),
        ),
    ]
