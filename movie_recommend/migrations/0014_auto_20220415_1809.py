# Generated by Django 3.2.12 on 2022-04-15 10:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movie_recommend', '0013_auto_20220415_1807'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='movie_time',
            field=models.CharField(default='', max_length=64),
        ),
        migrations.AlterField(
            model_name='movielens',
            name='movie_time',
            field=models.CharField(default='', max_length=64),
        ),
    ]
