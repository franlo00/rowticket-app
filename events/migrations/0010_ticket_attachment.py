# Generated by Django 4.1.4 on 2023-05-04 21:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0009_ticket_row'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='attachment',
            field=models.ImageField(default='', upload_to='', verbose_name='imagen'),
        ),
    ]
