from django.urls import path
from . import views

app_name = 'library'

urlpatterns = [
    path('', views.lista_libros, name='lista_libros'),
    path('<int:pk>/', views.detalle_libro, name='detalle_libro'),
]
