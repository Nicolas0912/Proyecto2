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

from ProyectoDjangoReservas.views import View_Inicio, View_Servicios, Crear_Usuario, View_Login, LogoutUser, Listado_Usuarios, Actualizar_Usuarios, Eliminar_Usuario, Crear_Servicio, Listado_Servicios, Actualizar_Servicios, Eliminar_Servicio, Estado_Servicios, servicios_ocultos

urlpatterns = [
    path('admin/', admin.site.urls),

    path('Index/Home', View_Inicio),
    path('Servicios/Index', View_Servicios, name='Servicios/Index'),
    path('Login/IniciarSesion', View_Login),
    path('Logout', LogoutUser),
    path('Usuarios/ListadoUser', Listado_Usuarios),

    
    path('Login/CrearUser', Crear_Usuario),
    path('Usuario/Actualizar/<int:id>',Actualizar_Usuarios),
    path('Usuario/Eliminar/<int:id>',Eliminar_Usuario),

    path('Servicio/Agregar',Crear_Servicio),
    path('Servicios/Listado',Listado_Servicios),
    path('Servicio/Actualizar/<int:id>',Actualizar_Servicios),
    path('Servicio/Eliminar/<int:id>',Eliminar_Servicio),
    path('Servicio/Estado/<int:id>',Estado_Servicios, name='/Servicio/Estado/'),
    path('Servicios/Ocultos', servicios_ocultos, name='/Servicios/Ocultos')

]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)