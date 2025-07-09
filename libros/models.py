from django.db import models
from django.contrib.auth.models import User

class Genero(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

class Autor(models.Model):
    nombre = models.CharField(max_length=100)
    nacionalidad = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

class Libro(models.Model):
    titulo = models.CharField(max_length=200)
    fecha_lanzamiento = models.DateField()
    book_url = models.FileField(upload_to='libros/')
    genero = models.ForeignKey(Genero, on_delete=models.CASCADE, related_name='libros')
    autor = models.ForeignKey(Autor, on_delete=models.CASCADE, related_name='libros')
    creador = models.ForeignKey(User, on_delete=models.CASCADE, related_name='libros')

    def __str__(self):
        return self.titulo

class Puntuacion(models.Model):
    libro = models.ForeignKey(Libro, on_delete=models.CASCADE, related_name='puntuaciones')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='puntuaciones')
    puntuacion = models.IntegerField()
    comentario = models.TextField(blank=True)

    def __str__(self):
        return f'{self.usuario.username} - {self.libro.titulo} - {self.puntuacion}'
