# Generated by Django 4.2.7 on 2023-11-27 05:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_alter_customuser_groups'),
    ]

    operations = [
        migrations.CreateModel(
            name='Object',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100)),
            ],
        ),
    ]
