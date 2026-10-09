from django.shortcuts import render, get_object_or_404
from .models import Article, Category


def home(request):
    articles = Article.objects.select_related('author').prefetch_related('categories').all()
    return render(request, 'news/home.html', {'articles': articles})


def article_detail(request, slug):
    article = get_object_or_404(
        Article.objects.select_related('author').prefetch_related('categories'),
        slug=slug
    )
    return render(request, 'news/article_detail.html', {'article': article})


def category_list(request, slug):
    category = get_object_or_404(Category, slug=slug)
    articles = Article.objects.filter(categories=category).select_related('author').prefetch_related('categories')
    return render(request, 'news/category_list.html', {'category': category, 'articles': articles})