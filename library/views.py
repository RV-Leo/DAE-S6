from django.shortcuts import render, get_object_or_404
from .models import Book


def lista_libros(request):
    """List all books with related data."""
    books = Book.objects.all().select_related('autor').prefetch_related('categorias', 'publications__editorial')
    return render(request, 'library/book_list.html', {'books': books})


def detalle_libro(request, pk):
    """Detail view for a single book showing author, categories, and publisher info."""
    book = get_object_or_404(
        Book.objects.select_related('autor__profile'),
        pk=pk
    )
    categorias = book.categorias.all()
    publicaciones = book.publications.all()
    editoriales = [
        (pub.editorial, pub.fecha_publicacion, pub.edicion)
        for pub in publicaciones
    ]
    return render(request, 'library/book_detail.html', {
        'book': book,
        'categorias': categorias,
        'editoriales': editoriales,
    })
