# Generated by Django 4.1.4 on 2023-08-11 22:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0006_sellerticket'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('in_progress', 'En proceso'), ('pending_payment_confirmation', 'Esperando confirmación de pago'), ('on_hold', 'A la espera'), ('completed', 'Completada'), ('paid', 'Paga'), ('cancelled', 'Cancelada')], max_length=50, verbose_name='estado'),
        ),
    ]
