# Generated by Django 2.1.7 on 2019-02-21 07:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='user_ip',
            field=models.GenericIPAddressField(blank=True, null=True),
        ),
    ]
