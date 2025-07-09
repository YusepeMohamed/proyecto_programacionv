import matplotlib
matplotlib.use('Agg') 

import matplotlib.pyplot as plt
import seaborn as sns

from django.db.models import Count
from django.db import models
from django.db.models import Avg
from django.contrib.auth.models import User
from django.http import HttpResponse
from libros.models import Libro, Genero, Autor, Puntuacion
from collections import Counter
from io import BytesIO
import io

def libros_por_genero_horizontal(request):
    sns.set(style="whitegrid")
    generos = Genero.objects.annotate(cantidad=models.Count('libros')).order_by('cantidad')  # Orden ascendente para horizontal
    nombres = [g.nombre for g in generos]
    cantidades = [g.cantidad for g in generos]

    plt.figure(figsize=(10, 8))
    bars = plt.barh(nombres, cantidades, color=sns.color_palette('pastel'))

    plt.xlabel('Cantidad de Libros')
    plt.ylabel('Género')
    plt.title('Cantidad de Libros por Género')

    # Agregar valores al final de cada barra
    for i, (bar, cantidad) in enumerate(zip(bars, cantidades)):
        plt.text(cantidad + 0.1, i, str(int(cantidad)), va='center', fontsize=9)

    plt.tight_layout()
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png', dpi=300, bbox_inches='tight')
    plt.close()
    buffer.seek(0)
    return HttpResponse(buffer.getvalue(), content_type='image/png')






def promedio_puntuacion_libros(request):
    sns.set(style="whitegrid")
    libros = Libro.objects.prefetch_related('puntuaciones').all()

    nombres = []
    promedios = []

    for libro in libros:
        puntuaciones = libro.puntuaciones.all()
        if puntuaciones.exists():
            promedio = sum(p.puntuacion for p in puntuaciones) / puntuaciones.count()
            nombres.append(libro.titulo[:20])  # limitar nombre largo
            promedios.append(round(promedio, 2))

    plt.figure(figsize=(10, 6))
    bars = plt.bar(nombres, promedios, color=sns.color_palette('pastel'))

    plt.xlabel('Libro')
    plt.ylabel('Promedio de Puntuación')
    plt.title('Promedio de Puntuaciones por Libro')
    plt.xticks(rotation=45, ha='right')

    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2, height + 0.05, f"{height:.2f}", ha='center', fontsize=9)

    plt.tight_layout()
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    plt.close()
    buffer.seek(0)
    return HttpResponse(buffer.getvalue(), content_type='image/png')





def promedio_puntuacion_autores(request):
    sns.set(style="whitegrid")
    autores = Autor.objects.prefetch_related('libros__puntuaciones').all()

    nombres = []
    promedios = []

    for autor in autores:
        puntuaciones = []
        for libro in autor.libros.all():
            puntuaciones.extend(libro.puntuaciones.values_list('puntuacion', flat=True))
        if puntuaciones:
            promedio = sum(puntuaciones) / len(puntuaciones)
            nombres.append(autor.nombre[:20])  # truncar si es largo
            promedios.append(round(promedio, 2))

    plt.figure(figsize=(10, 6))
    bars = plt.bar(nombres, promedios, color=sns.color_palette('pastel'))

    plt.xlabel('Autor')
    plt.ylabel('Promedio de Puntuación')
    plt.title('Promedio de Puntuaciones por Autor')
    plt.xticks(rotation=45, ha='right')

    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2, height + 0.05, f"{height:.2f}", ha='center', fontsize=9)

    plt.tight_layout()
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    plt.close()
    buffer.seek(0)
    return HttpResponse(buffer.getvalue(), content_type='image/png')







def libros_por_nacionalidad(request):
    sns.set(style="whitegrid")  # Estilo limpio y claro
    autores = Autor.objects.prefetch_related('libros')
    
    # Contar cuántos libros hay por nacionalidad
    nacionalidades = []
    for autor in autores:
        nacionalidades.extend([autor.nacionalidad] * autor.libros.count())

    conteo = Counter(nacionalidades)
    nacionalidades_ordenadas = list(conteo.keys())
    cantidades = list(conteo.values())

    # Crear gráfico
    plt.figure(figsize=(10, 6))
    bars = plt.barh(nacionalidades_ordenadas, cantidades, color=sns.color_palette('pastel'))

    plt.xlabel('Cantidad de Libros')
    plt.ylabel('Nacionalidad del Autor')
    plt.title('Cantidad de Libros por Nacionalidad del Autor')

    # Mostrar los valores al final de cada barra
    for bar in bars:
        width = bar.get_width()
        plt.text(width + 0.1, bar.get_y() + bar.get_height() / 2, str(int(width)), va='center', fontsize=9)

    plt.tight_layout()

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    plt.close()
    buffer.seek(0)

    return HttpResponse(buffer.getvalue(), content_type='image/png')




def libros_por_usuario(request):
    sns.set(style="whitegrid")  # Estilo limpio

    # Obtener usuarios con libros
    usuarios = User.objects.prefetch_related('libros')
    datos = {usuario.username: usuario.libros.count() for usuario in usuarios if usuario.libros.count() > 0}

    if not datos:
        return HttpResponse("No hay datos suficientes para generar el gráfico.", content_type="text/plain")

    usuarios = list(datos.keys())
    cantidades = list(datos.values())

    plt.figure(figsize=(10, 6))
    bars = plt.barh(usuarios, cantidades, color=sns.color_palette('pastel'))

    plt.xlabel('Cantidad de Libros')
    plt.ylabel('Usuario')
    plt.title('Libros Creados por Usuario')

    for bar in bars:
        width = bar.get_width()
        plt.text(width + 0.1, bar.get_y() + bar.get_height() / 2, str(int(width)), va='center', fontsize=9)

    plt.tight_layout()
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    plt.close()
    buffer.seek(0)

    return HttpResponse(buffer.getvalue(), content_type='image/png')




