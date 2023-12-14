# Generated by Django 4.2.2 on 2023-12-14 10:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_colorvariant_sizevariant_product_color_variant_and_more'),
        ('accounts', '0003_alter_cart_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartitem',
            name='color',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='products.colorvariant'),
        ),
        migrations.AlterField(
            model_name='cartitem',
            name='size',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='products.sizevariant'),
        ),
    ]