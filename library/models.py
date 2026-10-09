from django.db import models


class Author(models.Model):
    """Book author with personal information."""
    nombre = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    bio = models.TextField(blank=True)
    fecha_nacimiento = models.DateField(blank=True, null=True)

    class Meta:
        verbose_name = 'Author'
        verbose_name_plural = 'Authors'

    def __str__(self):
        return self.nombre


class AuthorProfile(models.Model):
    """Author profile with biographical data, linked 1:1 with Author."""
    author = models.OneToOneField(Author, on_delete=models.CASCADE, related_name='profile')
    direccion = models.CharField(max_length=300, blank=True)
    telefono = models.CharField(max_length=20, blank=True)
    foto = models.ImageField(upload_to='authors/', blank=True, null=True)

    class Meta:
        verbose_name = 'Author Profile'
        verbose_name_plural = 'Author Profiles'

    def __str__(self):
        return f"Profile of {self.author.nombre}"


class Category(models.Model):
    """Book category for classification."""
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.nombre


class Publisher(models.Model):
    """Book publisher."""
    nombre = models.CharField(max_length=200, unique=True)
    direccion = models.CharField(max_length=300, blank=True)
    ciudad = models.CharField(max_length=100, blank=True)
    sitio_web = models.URLField(blank=True)

    class Meta:
        verbose_name = 'Publisher'
        verbose_name_plural = 'Publishers'

    def __str__(self):
        return self.nombre


class Publication(models.Model):
    """Through model for Book-Publisher relationship with custom attributes."""
    libro = models.ForeignKey('Book', on_delete=models.CASCADE, related_name='publications')
    editorial = models.ForeignKey(Publisher, on_delete=models.PROTECT, related_name='publications')
    fecha_publicacion = models.DateField()
    edicion = models.CharField(max_length=50, blank=True)

    class Meta:
        verbose_name = 'Publication'
        verbose_name_plural = 'Publications'
        unique_together = ('libro', 'editorial')

    def __str__(self):
        return f"{self.libro.titulo} - {self.editorial.nombre}"


class Book(models.Model):
    """Book with relationships to Author, Category, and Publisher."""
    titulo = models.CharField(max_length=300)
    isbn = models.CharField(max_length=13, unique=True)
    autor = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')
    categorias = models.ManyToManyField(Category, related_name='books')
    editorial = models.ManyToManyField(
        Publisher,
        through='Publication',
        through_fields=('libro', 'editorial'),
        related_name='books',
    )
    fecha_publicacion = models.DateField(blank=True, null=True)
    sinopsis = models.TextField(blank=True)
    portada = models.ImageField(upload_to='books/', blank=True, null=True)

    class Meta:
        verbose_name = 'Book'
        verbose_name_plural = 'Books'
        ordering = ['titulo']

    def __str__(self):
        return self.titulo
