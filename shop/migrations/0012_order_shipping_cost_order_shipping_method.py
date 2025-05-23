# Generated by Django 5.1.7 on 2025-04-16 18:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0011_order_orderitem'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='shipping_cost',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=6),
        ),
        migrations.AddField(
            model_name='order',
            name='shipping_method',
            field=models.CharField(choices=[('standard', 'Standard'), ('express', 'Express')], default='standard', max_length=10),
        ),
    ]
