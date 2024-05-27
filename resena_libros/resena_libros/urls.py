"""
URL configuration for resena_libros project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from resena_libros_web.views import inicio, registro_usuario, iniciar_sesion, cerrar_sesion, libros, detalle_libro, busqueda, busqueda_autor,busqueda_categoria,busqueda_calificacion, agregar_libro, contacto, contacto_exitoso

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', inicio, name="inicio"),
    path('home', inicio, name="inicio"),
    path('registro', registro_usuario, name="registro_usuario"),
    path('iniciar_sesion', iniciar_sesion, name="iniciar_sesion"),
    path('cerrar_sesion', cerrar_sesion, name="cerrar_sesion"),
    path('libros', libros, name="libros"),
    path('contacto', contacto, name="contacto"),
    path('contacto_exitoso', contacto_exitoso, name="contacto_exitoso"),
    path('libros/agregar_libro', agregar_libro, name="agregar_libro"),
    path('detalle_libro/<int:libro_id>/resena', detalle_libro, name='detalle_libro'),
    path('busqueda', busqueda, name="busqueda"),
    path('busqueda/busqueda_autor', busqueda_autor, name="busqueda_autor"),
    path('busqueda/busqueda_categoria', busqueda_categoria, name="busqueda_categoria"),
    path('busqueda/busqueda_calificacion', busqueda_calificacion, name="busqueda_calificacion"),
    path('accounts/', include('django.contrib.auth.urls'))
]
