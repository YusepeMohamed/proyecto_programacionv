from django.urls import path
from . import views

urlpatterns = [
    # Generos
    path('generos/', views.genero_list_create, name='genero_list_create'),
    path('generos/<int:pk>/', views.genero_detail, name='genero_detail'),

    # Autores
    path('autores/', views.autor_list_create, name='autor_list_create'),
    path('autores/<int:pk>/', views.autor_detail, name='autor_detail'),

    # Libros
    path('libros/', views.libro_list_create, name='libro_list_create'),
    path('libros/<int:pk>/', views.libro_detail, name='libro_detail'),

    # Puntuaciones
    path('puntuaciones/', views.puntuacion_list_create, name='puntuacion_list_create'),
    path('puntuaciones/<int:pk>/', views.puntuacion_detail, name='puntuacion_detail'),
]
