# Generated by Django 4.1.4 on 2023-08-28 21:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0025_alter_organizer_header_image_and_more'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='ticket',
            index=models.Index(fields=['seller'], name='events_tick_seller__b674e2_idx'),
        ),
    ]
