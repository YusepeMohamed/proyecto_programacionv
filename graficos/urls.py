from django.urls import path
from . import views

urlpatterns = [
    path('libros-por-genero/', views.libros_por_genero_horizontal, name='libros_por_genero'),
    path('promedio-puntuacion-libros/', views.promedio_puntuacion_libros, name='promedio_puntuacion_libros'),
    path('promedio-puntuacion-autores/', views.promedio_puntuacion_autores, name='promedio-puntuacion-autores'),
    path('libros-por-nacionalidad/', views.libros_por_nacionalidad, name='libros-por-nacionalidad'),
    path('libros-por-usuario/', views.libros_por_usuario, name='libros_por_usuario'),


]
