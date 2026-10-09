from django.contrib import admin
from .models import Author, AuthorProfile, Book, Category, Publisher, Publication


class AuthorProfileInline(admin.StackedInline):
    model = AuthorProfile
    can_delete = False
    verbose_name_plural = 'Profile'


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'email')
    search_fields = ('nombre', 'email')
    inlines = [AuthorProfileInline]


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'autor', 'fecha_publicacion')
    search_fields = ('titulo', 'isbn')
    filter_horizontal = ('categorias',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    search_fields = ('nombre',)


class PublicationInline(admin.TabularInline):
    model = Publication
    extra = 0


@admin.register(Publisher)
class PublisherAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'ciudad', 'sitio_web')
    search_fields = ('nombre', 'ciudad')
    inlines = [PublicationInline]


@admin.register(Publication)
class PublicationAdmin(admin.ModelAdmin):
    list_display = ('libro', 'editorial', 'fecha_publicacion', 'edicion')
    list_filter = ('fecha_publicacion',)
