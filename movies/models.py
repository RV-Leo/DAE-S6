from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Genre(models.Model):
    """Movie genre used to classify and recommend movies."""
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        verbose_name = 'Genre'
        verbose_name_plural = 'Genres'
        ordering = ['name']

    def __str__(self):
        return self.name


class Person(models.Model):
    """Film crew member; used as the director of a movie."""
    name = models.CharField(max_length=150)
    birth_date = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to='people/', blank=True, null=True)

    class Meta:
        verbose_name = 'Person'
        verbose_name_plural = 'People'
        ordering = ['name']

    def __str__(self):
        return self.name


class Movie(models.Model):
    """Movie in the catalog, linked to its genres (M2M) and director (FK)."""
    title = models.CharField(max_length=200)
    year = models.PositiveSmallIntegerField()
    synopsis = models.TextField(blank=True)
    poster = models.ImageField(upload_to='posters/', blank=True, null=True)
    director = models.ForeignKey(
        Person,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='directed_movies',
    )
    genres = models.ManyToManyField(Genre, related_name='movies')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Movie'
        verbose_name_plural = 'Movies'
        ordering = ['title']

    def __str__(self):
        return f'{self.title} ({self.year})'


class Rating(models.Model):
    """User score for a movie, from 1 to 5."""
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='ratings')
    score = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
    )
    comment = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Rating'
        verbose_name_plural = 'Ratings'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.movie.title}: {self.score}/5'
