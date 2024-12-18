# M7-L1-AccesoADatosV2
Educativo y de Aprendizaje Personal Python  

---
## Tabla de Contenidos
- [Tecnologías](#Tecnologías)
- [Configuración Inicial](#configuración-Inicial)
- [Configuración Base de datos](#configuración-Base-de-datos)
- [Creación del Modelo](#creación-del-modelo)
- [Creación de Vistas](#creación-de-vistas)
- [Insertamos datos en un dataShell ](#Insertamos-datos-en-un-dataShell)
- [Configuracion de la vista de la base de datos](#Configuracion-de-la-vista-de-la-base-de-datos)
---
# Tecnologías
- Django: Framework web en Python.
- PostgreSQL: Base de datos relacional avanzada 
--- 
# Configuración Inicial 
1. Entorno virtual 
    ```bash 
    python -m venv venv

2. Activar el entorno virtual
    ```bash 
    venv\Scripts\activate

3. Instalar Django
    ```bash 
    pip install django 

4. Actulizamos el pip 
    ```bash
    python.exe -m pip install --upgrade pip

5. Crear el proyecto de django
    ```bash 
    django-admin startproject administracion_hotel 

6. Ingresamos al proyecto administracion_hotel 
    ```bash 
    cd administracion_hotel

7. Creamos la aplicacion llamada hotel
    ```bash 
    python manage.py startapp hotel

8. Configuración de administracion_hotel/settings.py 
    ```bash 
    INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'hotel',
    ]

# Configuración Base de datos
9. Instalar python-decouple: Es una biblioteca que ayuda manejar las variables de entorno 
    ```bash
    pip install python-decouple

10. Creamos el archivo .env a la altura del proyecto al lado manage.py 
    ```bash
    DATABASE_NAME=nombre_base_de_datos
    DATABASE_USER=postgres
    DATABASE_PASSWORD=yourpassword
    DATABASE_HOST=localhost
    DATABASE_PORT=5432

11. Configuracion de la base de datos ingresando los parametros de conexión 
    ```bash
    from decouple import config

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': config('DATABASE_NAME'),
            'USER': config('DATABASE_USER'),
            'PASSWORD': config('DATABASE_PASSWORD'),
            'HOST': config('DATABASE_HOST'),
            'PORT': config('DATABASE_PORT'),
        }
    }
11. Instalacion de psycopg2: es un adaptador de base de datos para Python que permite interactuar con bases de datos PostgreSQL
    ```bash
    pip install pyscopg2 

# Creación del Modelo 

12. en hotel/models.py
    ```bash
    from django.db import models

    # Create your models here.
    class Cliente(models.Model):
        nombre = models.CharField(max_length=100)
        apellido = models.CharField(max_length=100)
        correo = models.EmailField(unique=True)
        telefono = models.CharField(max_length=15)
        fecha_ingreso = models.DateField()
        fecha_salida = models.DateField()

        def __str__(self):
            return f"{self.nombre} - {self.apellido}"
        
    class Habitacion(models.Model):
        TIPO_HABITACION = [
            ('SIMPLE', 'Simple'),
            ('GRANDE', 'Grande'),
            ('SUITE', 'Suite'),
        ]

        numero_habitacion = models.CharField(max_length=10, unique=True)
        tipo_habitacion = models.CharField(max_length=10, choices=TIPO_HABITACION)
        precio_por_noche = models.DecimalField(max_digits=6, decimal_places=2)
        disponible = models.BooleanField(default=True)

        def __str__(self):
            return f"Habitacion {self.numero_habitacion} ({self.get_tipo_habitacion_display()})"

13. Ejecuta las migraciones para aplicar estos cambios a la base de datos:
    ```bash 
    python manage.py makemigrations
    python manage.py migrate

# Creación de Vistas

14. hotel/views.py 
    ```bash 
    from django.shortcuts import render
    from django.db import connection
    from .models import Cliente, Habitacion

    def habitacion_disponible_base_datos(request):
    # Ejecutar consulta SQL directa
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM hotel_habitacion WHERE disponible = TRUE")
        columnas = [col[0] for col in cursor.description]  # Obtener nombres de columnas
        filas = [dict(zip(columnas, fila)) for fila in cursor.fetchall()]  # Convertir filas a diccionarios
        # Renderizar la plantilla con los datos
        return render(request, 'habitaciones_db.html', {'habitaciones': filas})


    def lista_clientes_base_datos(request):
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM hotel_cliente ORDER BY fecha_ingreso DESC")
            columnas = [col[0] for col in cursor.description]  # Obtener nombres de columnas
            filas = [dict(zip(columnas, fila)) for fila in cursor.fetchall()]  # Convertir filas a diccionarios
            # Renderizar la plantilla con los datos
            return render(request, 'clientes_db.html', {'clientes': filas})

    # Consultas indirecta mediante el modelo a la Base de Datos 
    def habitacion_disponible(request):
        habitaciones = Habitacion.objects.raw('SELECT * FROM hotel_habitacion WHERE disponible = TRUE')
        return render(request, 'habitaciones.html', {'habitaciones': habitaciones})

    def lista_clientes(request):
        clientes = Cliente.objects.raw('SELECT * FROM hotel_cliente ORDER BY fecha_ingreso DESC')
        return render(request, 'clientes.html', {'clientes': clientes})

15. creamos en hotel/templates/clientes_db.html 
    ```bash 
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Clientes DB</title>
    </head>
    <body>
        <table>
            <h1>Clientes db</h1>
            <tr>
                <th>Nombre</th>
                <th>Apellido</th>
            </tr>
            {% for cliente in clientes %}
            <tr>
                <td>{{cliente.nombre}}</td>
                <td>{{cliente.apellido}}</td>
            </tr>
            {% endfor %}
        </table>
    </body>
    </html>
16. creamos en hotel/templates/clientes.html 
    ```bash 
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Clientes</title>
    </head>

    <body>
        <h1>Clientes Modelo</h1>
        <ul>
            {% for cliente in clientes %}
            <li>{{ cliente.nombre }}</li>
            {% endfor %}
        </ul>
    </body>
    </html>
17. creamos en hotel/templates/habitaciones_db.html 
    ```bash 
    <!DOCTYPE html>
    <html lang="en">

    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Habitaciones DB</title>
    </head>

    <body>
        <h1>Habitaciones DB</h1>
        <ul>
            {% for habitacion in habitaciones %}
            <li>{{ habitacion.numero_habitacion}}</li>
            {% endfor %}
        </ul>
    </body>
    </html>
18. creamos en hotel/templates/habitaciones.html 
    ```bash 
    <!DOCTYPE html>
    <html lang="en">

    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Habitaciones Modelo</title>
    </head>

    <body>
        <h1>Habitaciones Modelo</h1>
        <ul>
            {% for habitacion in habitaciones %}
            <li>{{ habitacion.numero_habitacion }}</li>
            {% endfor %}
        </ul>
    </body>

    </html>
19. administracion_hotel/urls.py 
    ```bash 
    from django.contrib import admin
    from django.urls import path
    from hotel import views

    urlpatterns = [
        path('admin/', admin.site.urls),
        path('clientesDB/', views.lista_clientes_base_datos, name='clientesDB'),
        path('clientes/', views.lista_clientes, name='clientes'),
        path('habitacionesDB/', views.habitacion_disponible_base_datos, name='habitacionesDB'),
        path('habitaciones/', views.habitacion_disponible, name='habitacion'),
    ]
# Insertamos datos en un dataShell 

20. Ingresar datos con el comando
    ```bash	
    python manage.py shell

21. Información de Ingresos de datos
    ```bash	
    from hotel.models import Cliente, Habitacion
    from datetime import date

    cliente1 = Cliente(
        nombre="Juan",
        apellido="Pérez",
        correo="juan.perez@example.com",
        telefono="123456789",
        fecha_ingreso=date(2024, 1, 1),
        fecha_salida=date(2024, 1, 7)
    )
    cliente1.save()

    cliente2 = Cliente(
        nombre="Ana",
        apellido="Gómez",
        correo="ana.gomez@example.com",
        telefono="987654321",
        fecha_ingreso=date(2024, 1, 3),
        fecha_salida=date(2024, 1, 10)
    )
    cliente2.save()

    cliente3 = Cliente(
        nombre="Carlos",
        apellido="López",
        correo="carlos.lopez@example.com",
        telefono="456123789",
        fecha_ingreso=date(2024, 1, 5),
        fecha_salida=date(2024, 1, 15)
    )
    cliente3.save()

    habitacion1 = Habitacion(
        numero_habitacion="101",
        tipo_habitacion="SIMPLE",
        precio_por_noche=50.00,
        disponible=True
    )
    habitacion1.save()

    habitacion2 = Habitacion(
        numero_habitacion="102",
        tipo_habitacion="GRANDE",
        precio_por_noche=100.00,
        disponible=False
    )
    habitacion2.save()

    habitacion3 = Habitacion(
        numero_habitacion="201",
        tipo_habitacion="SUITE",
        precio_por_noche=200.00,
        disponible=True
    )
    habitacion3.save()

    for cliente in Cliente.objects.all():
        print(cliente)

    for habitacion in Habitacion.objects.all():
        print(habitacion)

    exit()
# Configuracion de la vista de la base de datos
22. En hotel/admin.py 
    ```bash	
    from django.contrib import admin
    from .models import Cliente, Habitacion
    # Register your models here.
    admin.site.register(Cliente)
    admin.site.register(Habitacion)
