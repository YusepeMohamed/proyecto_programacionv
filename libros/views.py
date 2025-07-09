from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import Genero, Autor, Libro, Puntuacion
from .serializers import GeneroSerializer, AutorSerializer, LibroSerializer, PuntuacionSerializer

# ----------- CRUD GENERO -------------------
@api_view(['GET', 'POST'])
@permission_classes([permissions.IsAuthenticated])
def genero_list_create(request):
    if request.method == 'GET':
        generos = Genero.objects.all()
        serializer = GeneroSerializer(generos, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = GeneroSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([permissions.IsAuthenticated])
def genero_detail(request, pk):
    try:
        genero = Genero.objects.get(pk=pk)
    except Genero.DoesNotExist:
        return Response({'error': 'Género no encontrado'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = GeneroSerializer(genero)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = GeneroSerializer(genero, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        genero.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# ----------- CRUD AUTOR -------------------
@api_view(['GET', 'POST'])
@permission_classes([permissions.IsAuthenticated])
def autor_list_create(request):
    if request.method == 'GET':
        autores = Autor.objects.all()
        serializer = AutorSerializer(autores, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = AutorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([permissions.IsAuthenticated])
def autor_detail(request, pk):
    try:
        autor = Autor.objects.get(pk=pk)
    except Autor.DoesNotExist:
        return Response({'error': 'Autor no encontrado'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = AutorSerializer(autor)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = AutorSerializer(autor, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        autor.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# ----------- CRUD LIBRO -------------------
@api_view(['GET', 'POST'])
@permission_classes([permissions.IsAuthenticated])
def libro_list_create(request):
    if request.method == 'GET':
        libros = Libro.objects.all()
        serializer = LibroSerializer(libros, many=True, context={'request': request})
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = LibroSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(creador=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([permissions.IsAuthenticated])
def libro_detail(request, pk):
    try:
        libro = Libro.objects.get(pk=pk)
    except Libro.DoesNotExist:
        return Response({'error': 'Libro no encontrado'}, status=status.HTTP_404_NOT_FOUND)

    # Permiso extra: Solo el creador puede editar o borrar
    if request.method in ['PUT', 'DELETE'] and libro.creador != request.user:
        return Response({'error': 'No tienes permiso para modificar o borrar este libro.'}, status=status.HTTP_403_FORBIDDEN)

    if request.method == 'GET':
        serializer = LibroSerializer(libro, context={'request': request})
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = LibroSerializer(libro, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(creador=libro.creador)  # Mantener el creador original
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        libro.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# ----------- CRUD PUNTUACION -------------------
@api_view(['GET', 'POST'])
@permission_classes([permissions.IsAuthenticated])
def puntuacion_list_create(request):
    if request.method == 'GET':
        puntuaciones = Puntuacion.objects.all()
        serializer = PuntuacionSerializer(puntuaciones, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = PuntuacionSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(usuario=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([permissions.IsAuthenticated])
def puntuacion_detail(request, pk):
    try:
        puntuacion = Puntuacion.objects.get(pk=pk)
    except Puntuacion.DoesNotExist:
        return Response({'error': 'Puntuación no encontrada'}, status=status.HTTP_404_NOT_FOUND)

    # Permiso extra: Solo el autor puede modificar o borrar su puntuación
    if request.method in ['PUT', 'DELETE'] and puntuacion.usuario != request.user:
        return Response({'error': 'No tienes permiso para modificar o borrar esta puntuación.'}, status=status.HTTP_403_FORBIDDEN)

    if request.method == 'GET':
        serializer = PuntuacionSerializer(puntuacion)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = PuntuacionSerializer(puntuacion, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(usuario=puntuacion.usuario)  # Mantener autor original
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        puntuacion.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
