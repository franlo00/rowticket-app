# Generated by Django 4.1.4 on 2023-06-02 12:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_user_is_seller'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='is_seller',
        ),
    ]
