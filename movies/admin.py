from django.contrib import admin
from django.db.models import Avg, Count

from .models import Genre, Movie, Person, Rating


class RatingInline(admin.TabularInline):
    """Edit a movie's ratings without leaving the movie form."""
    model = Rating
    extra = 1
    fields = ('score', 'comment', 'created_at')
    readonly_fields = ('created_at',)


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'year', 'director', 'genre_list', 'average_score', 'rating_count')
    list_filter = ('genres', 'year')
    search_fields = ('title', 'director__name')
    filter_horizontal = ('genres',)
    readonly_fields = ('created_at', 'updated_at')
    inlines = [RatingInline]
    fieldsets = (
        (None, {'fields': ('title', 'year', 'director', 'genres')}),
        ('Details', {'fields': ('synopsis', 'poster')}),
        ('Audit', {'fields': ('created_at', 'updated_at')}),
    )

    def get_queryset(self, request):
        return (
            super().get_queryset(request)
            .select_related('director')
            .prefetch_related('genres')
            .annotate(avg_score=Avg('ratings__score'), num_ratings=Count('ratings', distinct=True))
        )

    @admin.display(description='Genres')
    def genre_list(self, obj):
        return ', '.join(genre.name for genre in obj.genres.all())

    @admin.display(description='Avg. score', ordering='avg_score')
    def average_score(self, obj):
        return f'{obj.avg_score:.1f}' if obj.avg_score is not None else '—'

    @admin.display(description='Ratings', ordering='num_ratings')
    def rating_count(self, obj):
        return obj.num_ratings


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'movie_count')
    search_fields = ('name',)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(num_movies=Count('movies'))

    @admin.display(description='Movies', ordering='num_movies')
    def movie_count(self, obj):
        return obj.num_movies


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ('name', 'birth_date')
    search_fields = ('name',)


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('movie', 'score', 'comment', 'created_at')
    list_filter = ('score',)
    search_fields = ('movie__title',)
    readonly_fields = ('created_at',)
    list_select_related = ('movie',)
