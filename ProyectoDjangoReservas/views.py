from django.db import connection
from django.conf import settings
from django.db.models import Q
import os
from django.shortcuts import render, get_object_or_404

from django.core.paginator import Paginator
from django.http import HttpResponse
from django.template import Template,Context
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout

from ProyectoDjangoReservas.models import Servicio
from ProyectoDjangoReservas.models import Galeria

#region Inicio

def View_Inicio (request):

    return render (request,'Index/Home.html')

#endregion


#region Servicios

def Estado_Servicios (request, id):
    servicio = Servicio.objects.get(id=id)

    # Cambiar el estado actual al estado opuesto
    servicio.estado = not servicio.estado

    servicio.save()

    return redirect ('/Servicios/Ocultos')

def servicios_ocultos(request):
    
    servicios_ocultos = Servicio.objects.filter(estado=False)

    return render(request, 'Servicios/ServiciosOcultos.html', {'servicio': servicios_ocultos})

def View_Servicios (request):

    categoria = request.GET.get('categoria')
    servicio = Servicio.objects.all()

    cantidad_servicios = Servicio.objects.count()

    if categoria:
        servicio = Servicio.objects.filter(
            Q(categoria__icontains = categoria)
        ).distinct()

    context = {'servicio':servicio,
               'cantidad_servicios': cantidad_servicios}

    return render (request,'Servicios/Index.html', context)

def Crear_Servicio (request):

    if request.method == 'POST':
        if request.POST.get('nombre') and request.FILES['foto'] and request.POST.get('descripcion') and request.POST.get('precio') and request.POST.get('categoria') and request.POST.get('estado'):

            servicio = Servicio()

            servicio.nombre = request.POST.get('nombre')
            img = request.FILES['foto']
            servicio.foto = img
            servicio.descripcion = request.POST.get('descripcion')
            servicio.precio = request.POST.get('precio')
            servicio.categoria = request.POST.get('categoria')
            estado = request.POST.get('estado')
            estado =  True if estado == 'True' else False
            servicio.estado = estado

            servicio.save()

            return redirect ('/Servicios/Index')

    return render (request, 'Servicios/AgregarServicio.html')

def Listado_Servicios (request):

    busqueda = request.GET.get('buscar')
    servicio = Servicio.objects.all()

    if busqueda:
        servicio = Servicio.objects.filter(
            Q(nombre__icontains = busqueda) | 
            Q(categoria__icontains = busqueda) | 
            Q(precio__icontains = busqueda)
        ).distinct()

    paginador = Paginator(servicio,5)
    pagina = request.GET.get('page') or 1
    servicio = paginador.get_page(pagina)
    current_page = int(pagina)

    paginas = range(1, servicio.paginator.num_pages + 1)

    context = { 'servicio':servicio,'current_page':current_page,'paginas':paginas}
    

    return render(request,'Servicios/ListadoServicios.html',context)

def Actualizar_Servicios (request, id):

    if request.method == 'POST':
        if request.POST.get('nombre') and request.FILES['foto'] and request.POST.get('descripcion') and request.POST.get('precio') and request.POST.get('categoria') and request.POST.get('estado'):
        
            servicio = Servicio.objects.get(id=id)

            ruta_foto = "media/"+str(servicio.foto)

            os.remove(ruta_foto)

            servicio.nombre = request.POST.get('nombre')
            img = request.FILES['foto']
            servicio.foto = img
            servicio.descripcion = request.POST.get('descripcion')
            servicio.precio = request.POST.get('precio')
            servicio.categoria = request.POST.get('categoria')
            estado = request.POST.get('estado')
            estado =  True if estado == 'True' else False
            servicio.estado = estado


            servicio.save()

            return redirect ('/Servicios/Index')
    else:
        servicio = Servicio.objects.filter(id=id)
        return render (request, 'Servicios/ActualizarServicio.html', {'servicio':servicio})

def Eliminar_Servicio (request, id):

    servicio = Servicio.objects.get(id=id)
    ruta_foto = "media/"+str(servicio.foto)

    os.remove(ruta_foto)
    servicio.delete()

    return redirect('/Servicios/Listado')
    
#endregion

#region Galeria

def View_Galeria (request):

    imagenes = Galeria.objects.all()
    
    context = {
        'imagenes':imagenes
    }

    return render (request,'Galeria/Index.html', context)

def Subir_imagenes (request):

    if request.method == 'POST':
        if request.FILES['url_imagen'] and request.POST.get('estado'):

            imagen = Galeria()
            
            img = request.FILES['url_imagen']
            imagen.url_imagen = img
            estado = request.POST.get('estado')
            estado =  True if estado == 'True' else False
            imagen.estado = estado

            imagen.save()
            
            return redirect ('/Galeria/Index')


    return render (request,'Galeria/SubirImagen.html')

def Listado_Imagenes (request):

    imagenes = Galeria.objects.all()

    paginador = Paginator(imagenes,5)
    pagina = request.GET.get('page') or 1
    imagenes = paginador.get_page(pagina)
    current_page = int(pagina)

    paginas = range(1, imagenes.paginator.num_pages + 1)

    context = { 'imagenes':imagenes,'current_page':current_page,'paginas':paginas}

    return render (request,'Galeria/ListadoImagenes.html', context)

def Estado_imagenes (request, id):

    imagenes = Galeria.objects.get(id=id)

    # Cambiar el estado actual al estado opuesto
    imagenes.estado = not imagenes.estado

    imagenes.save()

    return redirect ('/Galeria/ListadoImagenes')

def Eliminar_imagen (request,id):

    imagen = Galeria.objects.get(id=id)
    ruta_foto = "media/"+str(imagen.url_imagen)

    os.remove(ruta_foto)
    imagen.delete()

    return redirect ('/Galeria/ListadoImagenes')
#endregion

#region Login

def View_Login (request):
    if request.method == "POST":
        if request.POST.get('username') and request.POST.get('password'):
            user = authenticate(username = request.POST.get('username'), password = request.POST.get('password'))
            if user is not None:
                login(request, user)
                return redirect("/Index/Home")
            else:
                mensaje = "Correo o Contraseña Incorrecto"
        return render(request, 'Login/Login.html', {'mensaje': mensaje})
    else:
        return render(request, 'Login/Login.html')
    
def LogoutUser(request):
    logout(request)
    return redirect('/Login/IniciarSesion')

#endregion

#region Usuario

def Crear_Usuario (request):

    if request.method == 'POST':
        if request.POST.get('password') and request.POST.get('first_name') and request.POST.get('last_name') and request.POST.get('email'):

            Usuario = User.objects.create_user(username = request.POST.get('email'), email=request.POST.get('email'), password=request.POST.get('password'), first_name = request.POST.get('first_name'), last_name = request.POST.get('last_name'))
            Usuario.save()

            return redirect('/Login/IniciarSesion')
    else:
        return render (request,'Login/CrearUsuario.html')
    
def Listado_Usuarios (request):
    
    busqueda = request.GET.get('buscar')
    usuario = User.objects.all()

    if busqueda:
        usuario = User.objects.filter(
            Q(first_name__icontains = busqueda) | 
            Q(last_name__icontains = busqueda) | 
            Q(email__icontains = busqueda)
        ).distinct()

    paginador = Paginator(usuario,8)
    pagina = request.GET.get('page') or 1
    usuario = paginador.get_page(pagina)
    current_page = int(pagina)

    paginas = range(1, usuario.paginator.num_pages + 1)

    context = { 'usuario':usuario,'current_page':current_page,'paginas':paginas}
    

    return render(request,'Usuarios/ListadoUsuarios.html',context)

def Actualizar_Usuarios (request, id):

    if request.method == 'POST':
        if request.POST.get('first_name') and request.POST.get('last_name') and request.POST.get('email') and request.POST.get('is_superuser') and request.POST.get('is_active'):
            
            usuario = User.objects.get(id=id)

            usuario.first_name = request.POST.get('first_name')
            usuario.last_name = request.POST.get('last_name')
            usuario.email = request.POST.get('email')
            usuario.is_superuser = request.POST.get('is_superuser')
            usuario.is_active = request.POST.get('is_active')

            usuario.save()

            return redirect ('/Usuarios/ListadoUser')
    else:
        usuario = User.objects.filter(id=id)
        return render (request, 'Usuarios/ActualizarUsuarios.html', {'usuario':usuario})

def Eliminar_Usuario (request, id):

    usuario = User.objects.get(id=id)

    usuario.delete()

    return redirect('/Usuarios/ListadoUser')

#endregion

#region Reservas

def Reserva_Servicio (request,id):

    servicio = get_object_or_404(Servicio, id=id)

    context = {'servicio':servicio}


    return render (request,'Reservas/ReservarServicio.html',context)

#endregion