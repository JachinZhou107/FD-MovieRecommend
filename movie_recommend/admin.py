from django.contrib import admin

# Register your models here.
from .models import Movie, MovieIndex, MovieRating  # 这个需要我们自己导入相应的模型类（数据表）


class MovieAdmin(admin.ModelAdmin):
    list_display = ('movie_imdb_id','movie_name', 'movie_title', 'movie_time')
    search_fields = ('movie_name', 'movie_title', 'movie_time')


admin.site.register(Movie, MovieAdmin)
admin.site.register(MovieIndex)
admin.site.register(MovieRating)