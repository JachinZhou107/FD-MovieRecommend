from django.db import models


# Create your models here.
class MovieLens(models.Model):
    movie_name = models.CharField(max_length=255, default='')
    movie_time = models.CharField(max_length=64, null=True, blank=True)
    movie_title = models.CharField(max_length=128, null=True, blank=True)
    movie_poster = models.CharField(max_length=255, null=True, blank=True)
    movie_country = models.CharField(max_length=128, null=True, blank=True)
    movie_type = models.CharField(max_length=128, null=True, blank=True)
    movie_score = models.CharField(max_length=64, null=True, blank=True)
    movie_score_sum = models.CharField(max_length=64, null=True, blank=True)
    movie_length = models.CharField(max_length=32, null=True, blank=True)
    movie_director = models.CharField(max_length=128, null=True, blank=True)
    movie_actors = models.TextField(null=True, blank=True)
    movie_desc = models.TextField(null=True, blank=True)
    movie_db_url = models.CharField(max_length=128, default='none')
    movie_imdb_id = models.CharField(max_length=32, default='none')
    movie_update_time = models.DateField(default='2000-01-01')
    movie_other_name = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.movie_name


class Movie(models.Model):
    movie_name = models.CharField(max_length=255, default='')
    movie_time = models.CharField(max_length=64, null=True, blank=True)
    movie_title = models.CharField(max_length=128, null=True, blank=True)
    movie_poster = models.CharField(max_length=255, null=True, blank=True)
    movie_country = models.CharField(max_length=128, null=True, blank=True)
    movie_type = models.CharField(max_length=128, null=True, blank=True)
    movie_score = models.CharField(max_length=64, null=True, blank=True)
    movie_score_sum = models.CharField(max_length=64, null=True, blank=True)
    movie_length = models.CharField(max_length=32, null=True, blank=True)
    movie_director = models.CharField(max_length=128, null=True, blank=True)
    movie_actors = models.TextField(null=True, blank=True)
    movie_desc = models.TextField(null=True, blank=True)
    movie_db_url = models.CharField(max_length=128, default='none')
    movie_imdb_id = models.CharField(max_length=32, default='none')
    movie_update_time = models.DateField(default='2000-01-01')
    movie_other_name = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.movie_name+self.movie_title


class MovieRating(models.Model):
    movie_imdb_id = models.CharField(max_length=32, default='none')
    user_id = models.CharField(max_length=32, default='none')
    rating = models.DecimalField(max_digits=3, decimal_places=1, blank=True, null=True)
    comments = models.TextField(blank=True, null=True)
    time_stamp = models.CharField(max_length=32, default='1648699200')
    likes = models.IntegerField(default=0)

    def __str__(self):
        return self.user_id + ' ' + self.movie_imdb_id + ': ' + str(self.rating)
