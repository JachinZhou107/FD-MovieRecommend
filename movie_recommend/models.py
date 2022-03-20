from django.db import models

# Create your models here.
class Movie(models.Model):
    movie_name = models.CharField(max_length=128)
    movie_time = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.movie_name