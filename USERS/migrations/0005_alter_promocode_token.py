# Generated by Django 4.1 on 2022-10-11 05:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('USERS', '0004_alter_promocode_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='promocode',
            name='token',
            field=models.CharField(default=None, max_length=20),
        ),
    ]
