from django.db import models


# Create your models here.
class Movie(models.Model):
    movie_name = models.CharField(max_length=255, default='')
    movie_time = models.CharField(max_length=4, default='')
    movie_title = models.CharField(max_length=128, default='')
    movie_poster = models.CharField(max_length=128, default='')
    movie_country = models.CharField(max_length=128, default='')
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
        return self.movie_name+self.movie_title


class MovieIndex(models.Model):
    movie_title = models.CharField(max_length=255, default='')
    movie_imdb_id = models.CharField(max_length=32, default='none')
    movie_poster = models.CharField(max_length=255, default='')

    def __str__(self):
        return self.movie_title


class MovieRating(models.Model):
    movie_imdb_id = models.CharField(max_length=32, default='none')
    user_id = models.CharField(max_length=32, default='none')
    rating = models.DecimalField(max_digits=3, decimal_places=1, blank=True, null=True)
    comments = models.TextField(blank=True, null=True)
    time_stamp = models.CharField(max_length=32, default='1648699200')

    def __str__(self):
        return self.user_id + ' ' + self.movie_imdb_id + ': ' + str(self.rating)
