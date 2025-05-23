# Generated by Django 5.1.7 on 2025-04-15 18:44

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0005_remove_product_size_sizeoption'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='price',
            new_name='base_price',
        ),
        migrations.RemoveField(
            model_name='sizeoption',
            name='size',
        ),
        migrations.AddField(
            model_name='product',
            name='sizes',
            field=models.ManyToManyField(blank=True, related_name='products', to='shop.sizeoption'),
        ),
        migrations.AddField(
            model_name='sizeoption',
            name='code',
            field=models.CharField(choices=[('S', 'Small'), ('M', 'Medium'), ('L', 'Large'), ('XL', 'Extra Large')], default='S', max_length=2, unique=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='sizeoption',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='sizeoption',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='size_options', to='shop.product'),
        ),
    ]
