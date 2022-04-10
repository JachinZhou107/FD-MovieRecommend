from django.db import models


# Create your models here.
class Movie(models.Model):
    movie_name = models.CharField(max_length=255, default='')
    movie_time = models.CharField(max_length=4, default='')
    movie_title = models.CharField(max_length=128, default='')
    movie_poster = models.CharField(max_length=128, default='')
    movie_contry = models.CharField(max_length=128, default='')
    movie_type = models.CharField(max_length=128, default='')
    movie_score = models.CharField(max_length=64, default='')
    movie_score_sum = models.CharField(max_length=64, default='')
    movie_length = models.CharField(max_length=32, default='')
    movie_director = models.CharField(max_length=128, default='')
    movie_actors = models.TextField(default='')
    movie_desc = models.TextField(default='')
    movie_db_url = models.CharField(max_length=128, default='none')
    movie_imdb_id = models.CharField(max_length=32, default='none')
    movie_update_time = models.DateField(default='2000-01-01')
    def __str__(self):
        return self.movie_name


class Movie_index(models.Model):
    movie_title = models.CharField(max_length=128, default='')
    movie_imdb_id = movie_imdb_id = models.CharField(max_length=32, default='none')
    movie_poster = models.CharField(max_length=128, default='')
    def __str__(self):
        return self.movie_title