# Generated by Django 4.1.4 on 2023-05-09 23:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0011_ticket_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='attachment',
            field=models.ImageField(default='', null=True, upload_to='', verbose_name='imagen'),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='row',
            field=models.CharField(blank=True, default='', max_length=50, verbose_name='fila'),
        ),
    ]
