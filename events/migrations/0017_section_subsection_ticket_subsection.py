# Generated by Django 4.1.4 on 2023-06-26 23:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0016_event_individual_percentage_event_pay_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='subsection',
            field=models.CharField(blank=True, default='', max_length=50, verbose_name='subsector'),
        ),
    ]
