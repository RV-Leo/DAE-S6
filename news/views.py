from django.shortcuts import render
from .models import Article


def home(request):
    articles = Article.objects.select_related('author').prefetch_related('categories').all()
    return render(request, 'news/home.html', {'articles': articles})