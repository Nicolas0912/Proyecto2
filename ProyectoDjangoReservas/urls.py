"""
URL configuration for ProyectoDjangoReservas project.

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
from django.conf import settings
from django.conf.urls.static import static

from ProyectoDjangoReservas.views import View_Inicio, View_Servicios, Crear_Usuario, View_Login, LogoutUser, Listado_Usuarios, Actualizar_Usuarios, Eliminar_Usuario, Crear_Servicio, Listado_Servicios, Actualizar_Servicios, Eliminar_Servicio, Estado_Servicios, servicios_ocultos, View_Galeria, Subir_imagenes, Listado_Imagenes, Estado_imagenes, Eliminar_imagen, Reserva_Servicio, Listado_Reservas, Estado_Reserva, Reservas_Usuario, View_Restaurantes, Agregar_Restaurante, Listado_Restaurantes, Perfil_Usuarios, Estado_Usuario, Usuario_admin, View_Habitaciones, Agregar_Habitacion, Tipo_Habitacion, Listado_Habitaciones

urlpatterns = [
    path('admin/', admin.site.urls),

    path('Index/Home', View_Inicio),
    path('Servicios/Index', View_Servicios, name='Servicios/Index'),
    path('Login/IniciarSesion', View_Login),
    path('Logout', LogoutUser),
    path('Usuarios/ListadoUser', Listado_Usuarios),
    path('Galeria/Index', View_Galeria),
    path('Restaurantes/Index', View_Restaurantes),
    path('Habitaciones/Index',View_Habitaciones),

    
    path('Login/CrearUser', Crear_Usuario),
    path('Usuario/Actualizar/<int:id>',Actualizar_Usuarios),
    path('Usuario/Perfil/<int:id>',Perfil_Usuarios),
    path('Usuario/Eliminar/<int:id>',Eliminar_Usuario),
    path('Usuario/Estado/<int:id>',Estado_Usuario, name='/Usuario/Estado/'),
    path('Usuario/Admin/<int:id>',Usuario_admin, name='/Usuario/Admin/'),

    path('Servicio/Agregar',Crear_Servicio),
    path('Servicios/Listado',Listado_Servicios),
    path('Servicio/Actualizar/<int:id>',Actualizar_Servicios),
    path('Servicio/Eliminar/<int:id>',Eliminar_Servicio),
    path('Servicio/Estado/<int:id>',Estado_Servicios, name='/Servicio/Estado/'),
    path('Servicios/Ocultos', servicios_ocultos, name='/Servicios/Ocultos'),

    path('Galeria/SubirImagen',Subir_imagenes),
    path('Galeria/ListadoImagenes', Listado_Imagenes),  
    path('Galeria/Estado/<int:id>', Estado_imagenes, name='/Galeria/Estado/'),
    path('Galeria/Eliminar/<int:id>', Eliminar_imagen, name='/Galeria/Eliminar/'),

    path('Reservas/ReservarServicio/<int:id>', Reserva_Servicio),
    path('Reservas/ListadoReservas',Listado_Reservas),
    path('Reservas/Estado/<int:id>',Estado_Reserva, name='/Reservas/Estado/'),
    path('Reservas/MisReservas', Reservas_Usuario),

    path('Restaurantes/Agregar', Agregar_Restaurante),
    path('Restaurantes/Listado', Listado_Restaurantes),

    path('Habitacion/Agregar', Agregar_Habitacion),
    path('Habitacion/Tipo', Tipo_Habitacion),
    path('Habitaciones/Listado', Listado_Habitaciones)

]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)