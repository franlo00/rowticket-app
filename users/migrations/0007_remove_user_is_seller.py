# Generated by Django 4.1.4 on 2023-06-16 13:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_user_is_seller'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='is_seller',
        ),
    ]
