from django.db.models.deletion import ProtectedError
from django.test import TestCase, Client
from datetime import date
from .models import Author, AuthorProfile, Book, Category, Publisher, Publication


class AuthorModelTest(TestCase):
    """Tests for Author model."""

    def test_create_author(self):
        author = Author.objects.create(
            nombre="Test Author",
            email="test@test.com"
        )
        self.assertEqual(str(author), "Test Author")

    def test_author_str(self):
        author = Author.objects.create(nombre="Jane Austen", email="jane@austen.com")
        self.assertEqual(str(author), "Jane Austen")


class AuthorProfileModelTest(TestCase):
    """Tests for AuthorProfile model with OneToOneField."""

    def test_create_author_profile(self):
        author = Author.objects.create(nombre="Test", email="test@test.com")
        profile = AuthorProfile.objects.create(
            author=author,
            direccion="123 Main St",
            telefono="555-1234"
        )
        self.assertEqual(str(profile), f"Profile of {author.nombre}")
        self.assertEqual(profile.author, author)

    def test_one_to_one_relationship(self):
        author = Author.objects.create(nombre="Test", email="test@test.com")
        profile = AuthorProfile.objects.create(author=author, direccion="Test St")
        self.assertTrue(hasattr(author, 'profile'))
        self.assertEqual(author.profile, profile)


class CategoryModelTest(TestCase):
    """Tests for Category model."""

    def test_create_category(self):
        cat = Category.objects.create(nombre="Fiction", descripcion="Fictional literature")
        self.assertEqual(str(cat), "Fiction")


class PublisherModelTest(TestCase):
    """Tests for Publisher model."""

    def test_create_publisher(self):
        pub = Publisher.objects.create(nombre="Test Publisher", ciudad="Test City")
        self.assertEqual(str(pub), "Test Publisher")


class BookModelTest(TestCase):
    """Tests for Book model with relationships."""

    def setUp(self):
        self.author = Author.objects.create(nombre="Author", email="author@test.com")
        self.category = Category.objects.create(nombre="Category", descripcion="Desc")
        self.publisher = Publisher.objects.create(nombre="Pub", ciudad="City")

    def test_create_book(self):
        book = Book.objects.create(
            titulo="Test Book",
            isbn="1234567890123",
            autor=self.author
        )
        book.categorias.add(self.category)
        self.assertEqual(str(book), "Test Book")

    def test_book_author_relationship(self):
        book = Book.objects.create(
            titulo="Test Book",
            isbn="1234567890123",
            autor=self.author
        )
        self.assertEqual(book.autor.nombre, "Author")
        self.assertIn(book, self.author.books.all())


class PublicationModelTest(TestCase):
    """Tests for Publication through model."""

    def test_create_publication(self):
        author = Author.objects.create(nombre="A", email="a@test.com")
        publisher = Publisher.objects.create(nombre="P", ciudad="C")
        book = Book.objects.create(titulo="B", isbn="1234567890123", autor=author)
        pub = Publication.objects.create(
            libro=book,
            editorial=publisher,
            fecha_publicacion=date(2020, 1, 1),
            edicion="First"
        )
        self.assertEqual(str(pub), "B - P")

    def test_through_model_attributes(self):
        author = Author.objects.create(nombre="A", email="a@test.com")
        publisher = Publisher.objects.create(nombre="P", ciudad="C")
        book = Book.objects.create(titulo="B", isbn="1234567890123", autor=author)
        pub = Publication.objects.create(
            libro=book,
            editorial=publisher,
            fecha_publicacion=date(2020, 1, 1),
            edicion="Second"
        )
        self.assertEqual(pub.fecha_publicacion, date(2020, 1, 1))
        self.assertEqual(pub.edicion, "Second")


class ORMQueryTest(TestCase):
    """Tests for ORM queries in both directions."""

    def setUp(self):
        self.author = Author.objects.create(nombre="Gabriel", email="gabriel@test.com")
        self.profile = AuthorProfile.objects.create(
            author=self.author,
            direccion="Rancho",
            telefono="+57-123"
        )
        self.category1 = Category.objects.create(nombre="Magical Realism", descripcion="Genre")
        self.category2 = Category.objects.create(nombre="Fiction", descripcion="Fiction")
        self.publisher = Publisher.objects.create(nombre="Penguin", ciudad="London")

        self.book1 = Book.objects.create(
            titulo="100 Years of Solitude",
            isbn="1234567890123",
            autor=self.author,
            fecha_publicacion=date(1967, 5, 30)
        )
        self.book1.categorias.add(self.category1, self.category2)

        self.book2 = Book.objects.create(
            titulo="Love in Cholera",
            isbn="1234567890124",
            autor=self.author,
            fecha_publicacion=date(1985, 9, 1)
        )
        self.book2.categorias.add(self.category2)

        Publication.objects.create(
            libro=self.book1,
            editorial=self.publisher,
            fecha_publicacion=date(1967, 5, 30),
            edicion="First"
        )

    def test_book_to_author_query(self):
        """Forward query: Book -> Author via ForeignKey."""
        book = Book.objects.get(titulo="100 Years of Solitude")
        self.assertEqual(book.autor.nombre, "Gabriel")

    def test_author_to_books_query(self):
        """Reverse query: Author -> Books via related_name."""
        author = Author.objects.get(nombre="Gabriel")
        books = author.books.all()
        self.assertEqual(books.count(), 2)

    def test_manytomany_bidirectional(self):
        """ManyToMany relationship in both directions."""
        category = Category.objects.get(nombre="Magical Realism")
        books = category.books.all()
        self.assertIn(Book.objects.get(titulo="100 Years of Solitude"), books)

    def test_book_to_categories_query(self):
        """Forward query: Book -> Categories via ManyToManyField."""
        book = Book.objects.get(titulo="100 Years of Solitude")
        cats = book.categorias.all()
        self.assertEqual(cats.count(), 2)
        self.assertIn(self.category1, cats)
        self.assertIn(self.category2, cats)

    def test_through_model_query(self):
        """Query through model from Book side."""
        book = Book.objects.get(titulo="100 Years of Solitude")
        pubs = book.publications.all()
        self.assertEqual(pubs.count(), 1)
        self.assertEqual(pubs.first().editorial.nombre, "Penguin")

    def test_through_model_query_from_publisher(self):
        """Query through model from Publisher side."""
        publisher = Publisher.objects.get(nombre="Penguin")
        pubs = publisher.publications.all()
        self.assertEqual(pubs.count(), 1)

    def test_double_underscore_filter(self):
        """Filter with double underscore."""
        books = Book.objects.filter(categorias__nombre="Magical Realism")
        self.assertIn(Book.objects.get(titulo="100 Years of Solitude"), books)

    def test_profile_access(self):
        """Access author profile via OneToOne reverse relation."""
        author = Author.objects.get(nombre="Gabriel")
        self.assertIsNotNone(author.profile)
        self.assertEqual(author.profile.telefono, "+57-123")


class OnDeleteTest(TestCase):
    """Tests for on_delete behavior."""

    def test_cascade_delete_book_from_author(self):
        """CASCADE: Deleting author deletes related books."""
        author = Author.objects.create(nombre="ToDelete", email="del@test.com")
        book = Book.objects.create(titulo="ToDelete Book", isbn="1234567890123", autor=author)
        Author.objects.get(pk=author.pk).delete()
        self.assertFalse(Book.objects.filter(pk=book.pk).exists())

    def test_onetoone_delete_cascade(self):
        """OneToOne CASCADE: Deleting author also deletes profile."""
        author = Author.objects.create(nombre="Profile Author", email="profile@test.com")
        profile = AuthorProfile.objects.create(author=author, direccion="Test")
        Author.objects.get(pk=author.pk).delete()
        self.assertFalse(AuthorProfile.objects.filter(pk=profile.pk).exists())


class BookListViewTest(TestCase):
    """Tests for view responses."""

    def setUp(self):
        self.author = Author.objects.create(nombre="Author", email="author@test.com")
        self.book = Book.objects.create(titulo="Test Book", isbn="1234567890123", autor=self.author)

    def test_book_list_view(self):
        client = Client()
        response = client.get('/library/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Books")
        self.assertContains(response, "Test Book")

    def test_book_detail_view(self):
        client = Client()
        response = client.get(f'/library/{self.book.pk}/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Book")
        self.assertContains(response, "Author")


class OnDeleteProtectTest(TestCase):
    """Test that PROTECT on_delete prevents deletion."""

    def test_protect_behavior(self):
        """With PROTECT, deleting a publisher with publications should raise ProtectedError."""
        publisher = Publisher.objects.create(nombre="Protected Pub", ciudad="City")
        author = Author.objects.create(nombre="A", email="a@test.com")
        book = Book.objects.create(titulo="B", isbn="1234567890123", autor=author)
        Publication.objects.create(
            libro=book,
            editorial=publisher,
            fecha_publicacion=date(2020, 1, 1),
            edicion="First"
        )
        with self.assertRaises(ProtectedError):
            publisher.delete()
