#  API de Gestión de Libros - libros_site

![Python](https://img.shields.io/badge/python-3.11.9-blue.svg)
![Django](https://img.shields.io/badge/django-5.2.3-green.svg)
![PostgreSQL](https://img.shields.io/badge/postgresql-17-blue.svg)
![DRF](https://img.shields.io/badge/django--rest--framework-3.16.0-red.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Status](https://img.shields.io/badge/status-active-brightgreen.svg)

##  Descripción del Proyecto

Este proyecto es una **API REST desarrollada en Django** que permite gestionar una biblioteca digital donde los usuarios pueden registrarse, autenticarse y realizar operaciones CRUD sobre libros. El sistema incluye funcionalidades de valoración y comentarios, además de generar gráficos estadísticos con los datos almacenados.

### Características Principales:
- **Sistema de autenticación** con tokens
- **CRUD completo** para libros, autores, géneros y puntuaciones
- **Sistema de valoraciones** del 1 al 5 con comentarios
- **Generación de gráficos** estadísticos con matplotlib
- **Gestión de archivos** (subida de PDFs)
- **Permisos y restricciones** por usuario

---

##  Versiones de Herramientas y Librerías

### Herramientas Base
- **Python:** 3.11.9
- **Django:** 5.2.3
- **PostgreSQL:** 17
- **Django REST Framework:** 3.16.0

### Dependencias Principales
```
asgiref==3.8.1
Django==5.2.3
djangorestframework==3.16.0
djangorestframework-simplejwt==5.5.0
psycopg2-binary==2.9.10
PyJWT==2.9.0

# Librerías para gráficos
matplotlib==3.10.3
seaborn==0.13.2
numpy==2.3.1
pandas==2.3.0

# Utilidades
pillow==11.3.0
python-dateutil==2.9.0.post0
pytz==2025.2
```

---

##  Instalación

### 1. Prerequisitos
- Python 3.11.9 o superior
- PostgreSQL 17
- pip (gestor de paquetes de Python)

### 2. Configuración del Entorno Virtual
```bash
# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
venv\Scripts\activate

```

### 3. Instalación de Dependencias
```bash
# Instalar todas las dependencias
pip install Django==5.2.3
pip install djangorestframework==3.16.0
pip install djangorestframework-simplejwt==5.5.0
pip install psycopg2-binary==2.9.10
pip install matplotlib==3.10.3
pip install seaborn==0.13.2
pip install numpy==2.3.1
pip install pandas==2.3.0
pip install pillow==11.3.0
```

### 4. Configuración de Base de Datos
```bash
# Crear base de datos en PostgreSQL
createdb db_final_progra

# Configurar settings.py con tus credenciales de PostgreSQL
```

### 5. Creación del Proyecto Django
```bash
# Crear proyecto Django
django-admin startproject libros_site

# Crear las aplicaciones
python manage.py startapp libros
python manage.py startapp usuarios
python manage.py startapp graficos

# Ejecutar migraciones
python manage.py makemigrations
python manage.py migrate

# Crear superusuario
python manage.py createsuperuser

# Ejecutar servidor
python manage.py runserver
```

---

##  Estructura del Proyecto

El proyecto está organizado en **3 aplicaciones principales**:

###  Apps del Proyecto
```
libros_site/
├── libros/          # Gestión de libros, autores, géneros, puntuacion
├── usuarios/        # Autenticación y gestión de usuarios
├── graficos/        # Generación de gráficos estadísticos
└── libros_site/     # Configuración principal
```

###  Modelos de Datos

#### **Modelo Libro**
```python
class Libro(models.Model):
    titulo = models.CharField(max_length=200)
    fecha_lanzamiento = models.DateField()
    book_url = models.FileField(upload_to='libros/')
    genero = models.ForeignKey(Genero, on_delete=models.CASCADE)
    autor = models.ForeignKey(Autor, on_delete=models.CASCADE)
    creador = models.ForeignKey(User, on_delete=models.CASCADE)
```

#### **Modelo Autor**
```python
class Autor(models.Model):
    nombre = models.CharField(max_length=100)
    nacionalidad = models.CharField(max_length=100)
```

#### **Modelo Género**
```python
class Genero(models.Model):
    nombre = models.CharField(max_length=100)
```

#### **Modelo Puntuación**
```python
class Puntuacion(models.Model):
    libro = models.ForeignKey(Libro, on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    puntuacion = models.IntegerField()  # 1-5
    comentario = models.TextField(blank=True)
```

---

##  Funcionalidades Principales

###  Sistema de Autenticación
- Registro de usuarios con `django.contrib.auth`
- Login que genera **tokens de autenticación**
- Middleware de autenticación por token

###  Gestión de Libros (CRUD)

#### **Crear Libro**
```python
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def libro_list_create(request):
    serializer = LibroSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(creador=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
```

#### **Leer, Actualizar y Eliminar**
```python
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([permissions.IsAuthenticated])
def libro_detail(request, pk):
    libro = Libro.objects.get(pk=pk)
    
    # Solo el creador puede modificar o eliminar
    if request.method in ['PUT', 'DELETE'] and libro.creador != request.user:
        return Response({'error': 'Sin permisos'}, status=status.HTTP_403_FORBIDDEN)
    
    # Lógica para GET, PUT, DELETE...
```

---

##  Ejemplo de Uso con Postman

### **Crear un Libro**
**Método:** `POST`  
**URL:** `http://localhost:8000/api/libros/`  
**Headers:** `Authorization: Token tu_token_aqui`  
**Body:** `form-data`

| Key | Value | Type |
|-----|-------|------|
| titulo | Mi primer libro | Text |
| fecha_lanzamiento | 2024-01-15 | Text |
| genero | 1 | Text |
| autor | 1 | Text |
| book_url | (Archivo PDF) | File |

### **Respuesta Exitosa**
```json
{
    "id": 1,
    "creador": "usuario_ejemplo",
    "titulo": "Mi primer libro",
    "fecha_lanzamiento": "2024-01-15",
    "book_url": "/media/libros/mi_libro.pdf",
    "genero": 1,
    "autor": 1,
    "promedio_puntuacion": null
}
```

---

##  Listado de Libros

### **Obtener todos los libros**
**Método:** `GET`  
**URL:** `http://localhost:8000/api/libros/`  
**Headers:** `Authorization: Token tu_token_aqui`

### **Respuesta**
```json
[
    {
        "id": 1,
        "creador": "usuario1",
        "titulo": "El Quijote",
        "fecha_lanzamiento": "2024-01-15",
        "book_url": "/media/libros/quijote.pdf",
        "genero": 1,
        "autor": 1,
        "promedio_puntuacion": 4.5
    },
    {
        "id": 2,
        "creador": "usuario2",
        "titulo": "Cien años de soledad",
        "fecha_lanzamiento": "2024-02-20",
        "book_url": "/media/libros/cien_anos.pdf",
        "genero": 2,
        "autor": 2,
        "promedio_puntuacion": 4.8
    }
]
```

---

##  Documentación de Scripts para Gráficos

### **Script: Promedio de Puntuaciones por Autor**
Este script genera un gráfico de barras que muestra el promedio de puntuaciones de todos los libros por autor.

```python
def promedio_puntuacion_autores(request):
    """
    Genera un gráfico que muestra el promedio de puntuaciones por autor.
    Recorre todos los autores y calcula el promedio de las puntuaciones
    de todos sus libros.
    """
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
            nombres.append(autor.nombre[:20])
            promedios.append(round(promedio, 2))
    
    # Configuración del gráfico
    plt.figure(figsize=(10, 6))
    bars = plt.bar(nombres, promedios, color=sns.color_palette('pastel'))
    
    plt.xlabel('Autor')
    plt.ylabel('Promedio de Puntuación')
    plt.title('Promedio de Puntuaciones por Autor')
    plt.xticks(rotation=45, ha='right')
    
    # Mostrar valores en las barras
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2, height + 0.05, 
                f"{height:.2f}", ha='center', fontsize=9)
    
    plt.tight_layout()
    
    # Retornar imagen
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    plt.close()
    buffer.seek(0)
    return HttpResponse(buffer.getvalue(), content_type='image/png')
```

### **Script: Libros por Usuario**
```python
def libros_por_usuario(request):
    """
    Genera un gráfico horizontal que muestra la cantidad de libros
    creados por cada usuario registrado en el sistema.
    """
    usuarios = User.objects.prefetch_related('libros')
    datos = {usuario.username: usuario.libros.count() 
             for usuario in usuarios if usuario.libros.count() > 0}
    
    if not datos:
        return HttpResponse("No hay datos suficientes para generar el gráfico.", 
                          content_type="text/plain")
    
    usuarios = list(datos.keys())
    cantidades = list(datos.values())
    
    plt.figure(figsize=(10, 6))
    bars = plt.barh(usuarios, cantidades, color=sns.color_palette('pastel'))
    
    plt.xlabel('Cantidad de Libros')
    plt.ylabel('Usuario')
    plt.title('Libros Creados por Usuario')
    
    for bar in bars:
        width = bar.get_width()
        plt.text(width + 0.1, bar.get_y() + bar.get_height() / 2, 
                str(int(width)), va='center', fontsize=9)
    
    plt.tight_layout()
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    plt.close()
    buffer.seek(0)
    
    return HttpResponse(buffer.getvalue(), content_type='image/png')
```

---

##  Gráficos Disponibles

El sistema genera **5 tipos de gráficos estadísticos**:

### 1. **Cantidad de Libros por Género**
- **Endpoint:** `/graficos/libros-por-genero/`
- **Descripción:** Gráfico horizontal que muestra cuántos libros hay por cada género
- **Tipo:** Barras horizontales
![Image](https://github.com/user-attachments/assets/8da83dd0-448c-4d7f-8a2a-cd1d1c7876a1)

### 2. **Promedio de Puntuaciones por Libro**
- **Endpoint:** `/graficos/promedio-puntuacion-libros/`
- **Descripción:** Muestra el promedio de puntuaciones que ha recibido cada libro
- **Tipo:** Barras verticales
![Image](https://github.com/user-attachments/assets/9399038e-e29d-4116-b81d-c253283f508e)

### 3. **Promedio de Puntuaciones por Autor**
- **Endpoint:** `/graficos/promedio-puntuacion-autores/`
- **Descripción:** Calcula el promedio de puntuaciones de todos los libros por autor
- **Tipo:** Barras verticales
![Image](https://github.com/user-attachments/assets/7286449c-d7be-4229-8a50-69f3cbb32cdf)

### 4. **Libros por Nacionalidad del Autor**
- **Endpoint:** `/graficos/libros-por-nacionalidad/`
- **Descripción:** Distribución de libros según la nacionalidad de sus autores
- **Tipo:** Barras horizontales
![Image](https://github.com/user-attachments/assets/3a99392b-f372-4282-b515-9c7070e6c4c0)

### 5. **Libros Creados por Usuario**
- **Endpoint:** `/graficos/libros-por-usuario/`
- **Descripción:** Cantidad de libros que ha creado cada usuario
- **Tipo:** Barras horizontales
![Image](https://github.com/user-attachments/assets/bc264a09-a04e-45f0-8a75-a47d30206f34)

### **Tecnologías Utilizadas para Gráficos**
- **Matplotlib 3.10.3:** Generación de gráficos
- **Seaborn 0.13.2:** Estilos y paletas de colores
- **NumPy 2.3.1:** Operaciones matemáticas
- **Pandas 2.3.0:** Manipulación de datos

---

##  Sistema de Puntuaciones

### **Validaciones Implementadas**
- **Rango:** Las puntuaciones deben estar entre 1 y 5
- **Unicidad:** Un usuario solo puede puntuar un libro una vez
- **Autenticación:** Solo usuarios autenticados pueden puntuar
- **Edición:** Los usuarios pueden editar sus propias puntuaciones

### **Cálculo de Promedios**
```python
def get_promedio_puntuacion(self, obj):
    """Calcula el promedio de puntuaciones de un libro"""
    puntuaciones = obj.puntuaciones.all()
    if puntuaciones.exists():
        return round(sum(p.puntuacion for p in puntuaciones) / puntuaciones.count(), 2)
    return None
```

---

##  Arquitectura del Sistema

### **Configuración REST Framework**
```python
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
}
```

### **Aplicaciones Instaladas**
```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
    'usuarios',
    'libros',
    'graficos',
]
```

### **Gestión de Archivos**
```python
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
```

---

##  Licencias

Este proyecto utiliza las siguientes tecnologías y sus respectivas licencias:

### **Licencias de Software Base**
- **Python 3.11.9:** Python Software Foundation License
- **Django 5.2.3:** BSD 3-Clause License
- **PostgreSQL 17:** PostgreSQL License (similar a MIT)

### **Licencias de Librerías**
- **Django REST Framework:** BSD License
- **Django REST Framework SimpleJWT:** MIT License
- **Matplotlib:** Python Software Foundation License
- **Seaborn:** BSD 3-Clause License
- **NumPy:** BSD License
- **Pandas:** BSD 3-Clause License
- **Pillow:** PIL Software License
- **psycopg2-binary:** LGPL License

### **Licencia del Proyecto**
Este proyecto está distribuido bajo la **MIT License**.

---

##  Información del Desarrollador

- **Proyecto:** Trabajo Final 
- **Materia:** Programación 5
- **Tecnologías:** Python, Django, PostgreSQL, REST API
- **Año:** 2025

---

##  Próximas Funcionalidades

- [ ] Implementación de sugerencias por género basadas en valoraciones
- [ ] Búsqueda avanzada de libros
- [ ] Sistema de reseñas expandido
- [ ] Interfaz web frontend
- [ ] Notificaciones por email
- [ ] Integración con APIs externas de libros

---

##  Soporte

Para cualquier duda o problema, puedes:
- Revisar la documentación oficial de [Django](https://docs.djangoproject.com/)
- Consultar la documentación de [Django REST Framework](https://www.django-rest-framework.org/)
- Verificar la configuración de [PostgreSQL](https://www.postgresql.org/docs/)

---

**¡Gracias por usar nuestra API de Gestión de Libros!** 
