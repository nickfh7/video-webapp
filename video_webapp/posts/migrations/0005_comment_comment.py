# Generated by Django 2.1.7 on 2019-03-01 09:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0004_remove_comment_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='comment',
            field=models.TextField(default=1, verbose_name=''),
            preserve_default=False,
        ),
    ]
