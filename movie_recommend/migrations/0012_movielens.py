# Generated by Django 3.2.12 on 2022-04-15 10:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movie_recommend', '0011_movie_movie_other_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='MovieLens',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('movie_name', models.CharField(default='', max_length=255)),
                ('movie_time', models.CharField(default='', max_length=4)),
                ('movie_title', models.CharField(default='', max_length=128)),
                ('movie_poster', models.CharField(default='', max_length=128)),
                ('movie_country', models.CharField(default='', max_length=128)),
                ('movie_type', models.CharField(default='', max_length=128)),
                ('movie_score', models.CharField(default='', max_length=64)),
                ('movie_score_sum', models.CharField(default='', max_length=64)),
                ('movie_length', models.CharField(default='', max_length=32)),
                ('movie_director', models.CharField(default='', max_length=128)),
                ('movie_actors', models.TextField(default='')),
                ('movie_desc', models.TextField(default='')),
                ('movie_db_url', models.CharField(default='none', max_length=128)),
                ('movie_imdb_id', models.CharField(default='none', max_length=32)),
                ('movie_update_time', models.DateField(default='2000-01-01')),
                ('movie_other_name', models.CharField(default='', max_length=255)),
            ],
        ),
    ]
