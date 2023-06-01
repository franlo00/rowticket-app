# Generated by Django 4.1.4 on 2023-06-01 21:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0002_alter_paymentmethod_display_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paymentmethod',
            name='country',
            field=models.CharField(choices=[('ar', 'Argentina'), ('cl', 'Chile'), ('br', 'Brasil')], db_index=True, max_length=2, verbose_name='país'),
        ),
        migrations.AlterField(
            model_name='paymentmethod',
            name='display_name',
            field=models.CharField(max_length=255, verbose_name='Nombre para mostrar'),
        ),
    ]
