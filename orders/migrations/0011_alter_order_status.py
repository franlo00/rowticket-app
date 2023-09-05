# Generated by Django 4.1.4 on 2023-09-05 13:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0010_alter_order_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('in_progress', 'En proceso'), ('pending_payment_confirmation', 'Esperando confirmación de pago'), ('on_hold', 'A la espera'), ('completed', 'Completada'), ('paid', 'Pendiente de validación'), ('on_transit', 'En transito'), ('approved', 'Aprobada por el vendedor'), ('reserved', 'Reservada'), ('cancelled', 'Cancelada')], max_length=50, verbose_name='estado'),
        ),
    ]
