# Generated by Django 3.2.15 on 2022-09-03 07:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0004_auto_20220903_0651'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usersub',
            name='sub_id',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='usersub',
            name='user_id',
            field=models.IntegerField(),
        ),
    ]
