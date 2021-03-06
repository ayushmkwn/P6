# Generated by Django 3.2.6 on 2021-11-10 04:21

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='users',
            fields=[
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254, primary_key=True, serialize=False)),
                ('birthdate', models.DateField(blank=True, null=True)),
                ('gender', models.CharField(choices=[('Male', 'Male'), ('Female', 'Female'), ('Others', 'Others')], max_length=15)),
                ('mobileno', models.CharField(max_length=10, unique=True)),
                ('profilepic', models.ImageField(upload_to='profile_photos/')),
                ('user_creation_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('username', models.CharField(max_length=20, unique=True)),
                ('password', models.CharField(max_length=25)),
                ('is_authenticated', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
