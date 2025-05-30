# Generated by Django 5.1.4 on 2025-02-08 19:30

import AuthenticationSystem.models
import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Store_Industry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('store_industry', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('national_code', models.CharField(blank=True, max_length=10, null=True, unique=True, validators=[django.core.validators.RegexValidator(message='National code must be exactly 10 digits and contain only numbers.', regex='^\\d{10}$')])),
                ('store_logo', models.ImageField(blank=True, null=True, upload_to='store_logos/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['jpg', 'png', 'jpeg']), AuthenticationSystem.models.validate_file_size])),
                ('phone_number', models.CharField(max_length=15, unique=True, validators=[django.core.validators.RegexValidator(message='Phone number must start with +98 and be followed by 9 digits.', regex='^\\+98[0-9]{9}$')])),
                ('username', models.CharField(max_length=50, unique=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True, unique=True)),
                ('user_type', models.CharField(choices=[('customer', 'Customer'), ('store_owner', 'Store Owner'), ('admin', 'Admin')], default='customer', max_length=50)),
                ('active_mode', models.BooleanField(default=True)),
                ('store_description', models.TextField(blank=True, null=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='customuser_set', related_query_name='customuser', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='customuser_set', related_query_name='customuser', to='auth.permission', verbose_name='user permissions')),
                ('store_industry', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='AuthenticationSystem.store_industry')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
