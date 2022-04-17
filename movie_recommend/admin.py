from django.contrib import admin

# Register your models here.
from .models import Movie, MovieRating, MovieLens  # 这个需要我们自己导入相应的模型类（数据表）


class MovieAdmin(admin.ModelAdmin):
    list_display = ('id', 'movie_name', 'movie_title', 'movie_time', 'movie_imdb_id')
    search_fields = ('movie_name', 'movie_title', 'movie_time')


admin.site.register(Movie, MovieAdmin)
admin.site.register(MovieLens, MovieAdmin)
admin.site.register(MovieRating)
