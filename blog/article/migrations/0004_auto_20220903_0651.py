# Generated by Django 3.2.15 on 2022-09-03 06:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0003_alter_article_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserSub',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.IntegerField(unique=True)),
                ('sub_id', models.IntegerField(unique=True)),
            ],
        ),
        migrations.AlterModelOptions(
            name='article',
            options={'ordering': ['-time_update']},
        ),
    ]
