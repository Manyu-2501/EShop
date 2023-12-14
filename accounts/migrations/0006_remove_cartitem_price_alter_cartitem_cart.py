# Generated by Django 4.2.2 on 2023-12-14 14:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_alter_cartitem_product'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cartitem',
            name='price',
        ),
        migrations.AlterField(
            model_name='cartitem',
            name='cart',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cart_items', to='accounts.cart'),
        ),
    ]
