# Generated by Django 5.1.4 on 2025-02-26 00:12

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AuthenticationSystem', '0002_remove_customuser_store_industry'),
        ('Product', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='industry',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Product.industry'),
        ),
        migrations.DeleteModel(
            name='Store_Industry',
        ),
    ]
