from django.db.models import Avg, Count, F, Q
from django.shortcuts import get_object_or_404, render

from .models import Movie


def movie_list(request):
    """Public catalog with each movie's average score."""
    movies = (
        Movie.objects.select_related('director')
        .prefetch_related('genres')
        .annotate(avg_score=Avg('ratings__score'))
    )
    return render(request, 'movies/movie_list.html', {'movies': movies})


def recommendations(request, pk):
    """Best rated movies that share at least one genre with the given movie."""
    movie = get_object_or_404(Movie.objects.prefetch_related('genres'), pk=pk)
    genre_ids = [genre.id for genre in movie.genres.all()]

    similar_ids = (
        Movie.objects.filter(genres__in=genre_ids).exclude(pk=movie.pk).values('pk')
    )
    recommended = (
        Movie.objects.filter(pk__in=similar_ids)
        .select_related('director')
        .prefetch_related('genres')
        .annotate(
            avg_score=Avg('ratings__score'),
            shared_genres=Count('genres', filter=Q(genres__in=genre_ids), distinct=True),
        )
        .order_by(F('avg_score').desc(nulls_last=True), '-shared_genres', 'title')
    )
    return render(request, 'movies/recommendations.html', {
        'movie': movie,
        'recommended': recommended,
    })
