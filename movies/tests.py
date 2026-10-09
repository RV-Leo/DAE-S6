from django.contrib import admin
from django.contrib.auth.models import Group, User
from django.test import TestCase
from django.urls import reverse

from .admin import MovieAdmin
from .models import Genre, Movie, Person, Rating


class MovieModelTest(TestCase):

    def test_str_includes_year(self):
        movie = Movie.objects.create(title='Godzilla Minus One', year=2023)
        self.assertEqual(str(movie), 'Godzilla Minus One (2023)')

    def test_rating_str(self):
        movie = Movie.objects.create(title='Weapons', year=2025)
        rating = Rating.objects.create(movie=movie, score=4)
        self.assertEqual(str(rating), 'Weapons: 4/5')


class AdminConfigTest(TestCase):

    def test_all_models_registered(self):
        for model in (Movie, Genre, Person, Rating):
            self.assertTrue(admin.site.is_registered(model), model.__name__)

    def test_movie_admin_options(self):
        movie_admin = admin.site.get_model_admin(Movie)
        self.assertIsInstance(movie_admin, MovieAdmin)
        self.assertEqual(movie_admin.list_filter, ('genres', 'year'))
        self.assertIn('title', movie_admin.search_fields)
        self.assertEqual(movie_admin.readonly_fields, ('created_at', 'updated_at'))
        self.assertEqual(movie_admin.inlines[0].model, Rating)


class EditorsGroupTest(TestCase):
    """The 'editores' group is created by a data migration."""

    def setUp(self):
        self.editor = User.objects.create_user('editor', password='test-pass-123', is_staff=True)
        self.editor.groups.add(Group.objects.get(name='editores'))
        self.movie = Movie.objects.create(title='Alien: Romulus', year=2024)
        self.client.force_login(self.editor)

    def test_editor_can_add_and_change_but_not_delete(self):
        self.assertTrue(self.editor.has_perm('movies.add_movie'))
        self.assertTrue(self.editor.has_perm('movies.change_movie'))
        self.assertFalse(self.editor.has_perm('movies.delete_movie'))

    def test_editor_cannot_open_delete_page(self):
        url = reverse('admin:movies_movie_delete', args=[self.movie.pk])
        self.assertEqual(self.client.get(url).status_code, 403)

    def test_editor_cannot_manage_users(self):
        self.assertEqual(self.client.get(reverse('admin:auth_user_changelist')).status_code, 403)


class RecommendationViewTest(TestCase):

    def setUp(self):
        horror = Genre.objects.create(name='Terror')
        action = Genre.objects.create(name='Acción')
        scifi = Genre.objects.create(name='Ciencia ficción')

        self.resident_evil = Movie.objects.create(title='Resident Evil', year=2026)
        self.resident_evil.genres.set([horror, action])

        self.weapons = Movie.objects.create(title='Weapons', year=2025)
        self.weapons.genres.set([horror])
        Rating.objects.bulk_create([Rating(movie=self.weapons, score=s) for s in (5, 5)])

        self.endgame = Movie.objects.create(title='Avengers: Endgame', year=2019)
        self.endgame.genres.set([action])
        Rating.objects.create(movie=self.endgame, score=3)

        self.dune = Movie.objects.create(title='Dune: Part Two', year=2024)
        self.dune.genres.set([scifi])
        Rating.objects.create(movie=self.dune, score=5)

    def get_recommended(self, movie):
        response = self.client.get(reverse('movies:recommendations', args=[movie.pk]))
        self.assertEqual(response.status_code, 200)
        return list(response.context['recommended'])

    def test_only_same_genre_best_rated_first(self):
        self.assertEqual(self.get_recommended(self.resident_evil), [self.weapons, self.endgame])

    def test_excludes_the_movie_itself(self):
        self.assertNotIn(self.resident_evil, self.get_recommended(self.resident_evil))

    def test_unknown_movie_returns_404(self):
        response = self.client.get(reverse('movies:recommendations', args=[999]))
        self.assertEqual(response.status_code, 404)

    def test_view_is_public(self):
        response = self.client.get(reverse('movies:movie_list'))
        self.assertEqual(response.status_code, 200)
