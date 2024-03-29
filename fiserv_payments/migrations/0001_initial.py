# Generated by Django 4.1.4 on 2023-07-14 17:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('orders', '0006_sellerticket'),
        ('payments', '0004_merge_20230606_1201'),
    ]

    operations = [
        migrations.CreateModel(
            name='FiservPaymentMethod',
            fields=[
                ('paymentmethod_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='payments.paymentmethod')),
                ('api_key', models.CharField(max_length=255, verbose_name='API Key')),
                ('access_token', models.CharField(max_length=255, verbose_name='Access token')),
                ('test_mode', models.BooleanField(verbose_name='modo test')),
            ],
            options={
                'verbose_name': 'Método de pago Fiserv',
                'verbose_name_plural': 'Métodos de pago Fiserv',
            },
            bases=('payments.paymentmethod',),
        ),
        migrations.CreateModel(
            name='FiservPayment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('identifier', models.CharField(db_index=True, editable=False, max_length=10, unique=True, verbose_name='identificador')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='creado')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='modificado')),
                ('request_data', models.JSONField(verbose_name='data (request)')),
                ('response_data', models.JSONField(verbose_name='data (response)')),
                ('checkout_id', models.CharField(blank=True, db_index=True, max_length=255, unique=True, verbose_name='checkout ID')),
                ('order', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='fiserv_payments', to='orders.order', verbose_name='compra')),
                ('payment_method', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='fiserv_payments', to='fiserv_payments.fiservpaymentmethod', verbose_name='medio de pago')),
            ],
            options={
                'verbose_name': 'Pago Fiserv',
                'verbose_name_plural': 'Pagos Fiserv',
                'ordering': ('-created',),
            },
        ),
        migrations.CreateModel(
            name='FiservIPN',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('identifier', models.CharField(db_index=True, editable=False, max_length=10, unique=True, verbose_name='identificador')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='creado')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='modificado')),
                ('data', models.JSONField(verbose_name='data (request)')),
                ('payment', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='ipns', to='fiserv_payments.fiservpayment', verbose_name='Pago Fiserv')),
            ],
            options={
                'verbose_name': 'IPN Fiserv',
                'verbose_name_plural': 'IPNs Fiserv',
                'ordering': ('-created',),
            },
        ),
    ]
