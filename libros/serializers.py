from rest_framework import serializers
from .models import Genero, Autor, Libro, Puntuacion

class GeneroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genero
        fields = '__all__'

class AutorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Autor
        fields = '__all__'

class LibroSerializer(serializers.ModelSerializer):
    creador = serializers.ReadOnlyField(source='creador.username')
    promedio_puntuacion = serializers.SerializerMethodField()

    class Meta:
        model = Libro
        fields = [
            'id',
            'creador',
            'titulo',
            'fecha_lanzamiento',
            'book_url',
            'genero',
            'autor',
            'promedio_puntuacion',
        ]

    def get_promedio_puntuacion(self, obj):
        puntuaciones = obj.puntuaciones.all()
        if puntuaciones.exists():
            return round(sum(p.puntuacion for p in puntuaciones) / puntuaciones.count(), 2)
        return None

class PuntuacionSerializer(serializers.ModelSerializer):
    usuario = serializers.ReadOnlyField(source='usuario.username')

    class Meta:
        model = Puntuacion
        fields = '__all__'

    def validate_puntuacion(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError("La puntuación debe estar entre 1 y 5.")
        return value

    def validate(self, data):
        request = self.context['request']
        user = request.user
        libro = data.get('libro')

        if request.method == 'POST':
            existe = Puntuacion.objects.filter(libro=libro, usuario=user).exists()
            if existe:
                raise serializers.ValidationError("Ya has puntuado este libro. Puedes editar tu puntuación pero no crear una nueva.")
        return data
