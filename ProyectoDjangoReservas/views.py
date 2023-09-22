from django.db import connection
from django.conf import settings
from django.db.models import Q
import os, re
from django.shortcuts import render, get_object_or_404
from datetime import datetime
from django.core.files import File
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.template import Template,Context
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from ProyectoDjangoReservas.models import Servicio, Galeria, Restaurante, Profile

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

        # Separar los elementos de la cadena dias_dispo en una lista
    for c in servicios_ocultos:
        c.dias_dispo = c.dias_dispo.split("-")

    return render(request, 'Servicios/ServiciosOcultos.html', {'servicio': servicios_ocultos})

def View_Servicios(request):
    categoria = request.GET.get('categoria')
    servicio = Servicio.objects.all()
    cantidad_servicios = Servicio.objects.count()

    if categoria:
        servicio = Servicio.objects.filter(
            Q(categoria__icontains=categoria)
        ).distinct()
    
    # Separar los elementos de la cadena dias_dispo en una lista
    for c in servicio:
        c.dias_dispo = c.dias_dispo.split("-")

    context = {
        'servicio': servicio,
        'cantidad_servicios': cantidad_servicios
    }
    
    return render(request, 'Servicios/Index.html', context)

def Crear_Servicio(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        foto = request.FILES['foto']
        descripcion = request.POST.get('descripcion')
        precio = request.POST.get('precio')
        estado = request.POST.get('estado')
        min_personas = request.POST.get('min_personas')
        max_personas = request.POST.get('max_personas')
        categoria = request.POST.get('categoria')
        dias_dispo = '-'.join(request.POST.getlist('dias_dispo'))
        
        # Verificar que los campos no estén vacíos
        if not nombre or not foto or not descripcion or not precio or not estado or not min_personas or not max_personas or not categoria or not dias_dispo:
            messages.error(request, 'Por favor, complete todos los campos.')
            return redirect('/Servicio/Agregar')
        
        # Verificar la extensión del archivo de imagen
        ext = foto.name.split('.')[-1].lower()
        if ext not in ['jpg', 'jpeg', 'png']:
            messages.error(request, 'Formato de imagen no válido. Por favor, seleccione una imagen en formato JPEG, PNG o JPG.')
            return redirect('/Servicio/Agregar')
        
        # Verificar el tamaño de la imagen
        if foto.size > 400000:
            messages.error(request, 'El tamaño de la imagen no puede ser mayor a 400 KB.')
            return redirect('/Servicio/Agregar')
        
        # Verificar la longitud de la descripción
        if len(descripcion) > 500:
            messages.error(request, 'La descripción no puede superar los 500 caracteres.')
            return redirect('/Servicio/Agregar')
        
        # Verificar que el precio no sea un número negativo
        if float(precio) < 0:
            messages.error(request, 'El precio no puede ser un número negativo.')
            return redirect('/Servicio/Agregar')
        
        # Verificar que el número mínimo no sea negativo
        if int(min_personas) < 0:
            messages.error(request, 'El número mínimo de personas no puede ser negativo.')
            return redirect('/Servicio/Agregar')
        
        # Verificar que el número máximo no sea negativo
        if int(max_personas) < 0:
            messages.error(request, 'El número máximo de personas no puede ser negativo.')
            return redirect('/Servicio/Agregar')
        
        # Verificar que el número mínimo no sea mayor que el número máximo
        if int(min_personas) > int(max_personas):
            messages.error(request, 'El número mínimo de personas no puede ser mayor que el número máximo de personas.')
            return redirect('/Servicio/Agregar')
        
        # Crear el objeto Servicio
        servicio = Servicio(nombre=nombre, foto=foto, descripcion=descripcion, precio=precio, estado=estado, min_personas=min_personas, max_personas=max_personas, dias_dispo=dias_dispo, categoria=categoria)
        
        # Asignar el nombre único a la imagen
        servicio.foto.name = f'S_Img_{nombre}.{ext}'
        
        # Guardar el objeto Servicio
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

    # Separar los elementos de la cadena dias_dispo en una lista
    for c in servicio:
        c.dias_dispo = c.dias_dispo.split("-")

    paginador = Paginator(servicio,5)
    pagina = request.GET.get('page') or 1
    servicio = paginador.get_page(pagina)
    current_page = int(pagina)

    paginas = range(1, servicio.paginator.num_pages + 1)

    context = { 'servicio':servicio,'current_page':current_page,'paginas':paginas}
    

    return render(request,'Servicios/ListadoServicios.html',context)

def Actualizar_Servicios(request, id):
    if request.method == 'POST':
        if (
            request.POST.get('nombre')
            and request.FILES['foto']
            and request.POST.get('descripcion')
            and request.POST.get('precio')
            and request.POST.get('categoria')
            and request.POST.get('estado')
            and request.POST.get('min_personas')
            and request.POST.get('max_personas')
            and request.POST.get('dias_dispo')
        ):
            servicio = Servicio.objects.get(id=id)
            
            # Verificar si la foto existe
            if servicio.foto:
                ruta_foto = "media/" + str(servicio.foto)
                
                # Eliminar la foto existente
                if os.path.exists(ruta_foto):
                    os.remove(ruta_foto)
            
            # Verificar la extensión del archivo de imagen
            img = request.FILES['foto']
            ext = img.name.split('.')[-1].lower()
            if ext not in ['jpg', 'jpeg', 'png']:
                messages.error(request, 'Formato de imagen no válido. Por favor, seleccione una imagen en formato JPEG, PNG o JPG.')
                return redirect(f'/Servicio/Actualizar/{id}')

            # Verificar el tamaño de la imagen
            if img.size > 400000:
                messages.error(request, 'El tamaño de la imagen no puede ser mayor a 400 KB.')
                return redirect(f'/Servicio/Actualizar/{id}')
            
            # Verificar la longitud de la descripción
            descripcion = request.POST.get('descripcion')
            if len(descripcion) > 500:
                messages.error(request, 'La descripción no puede superar los 500 caracteres.')
                return redirect(f'/Servicio/Actualizar/{id}')
            
            # Verificar que el precio no sea un número negativo
            precio = request.POST.get('precio')
            if float(precio) < 0:
                messages.error(request, 'El precio no puede ser un número negativo.')
                return redirect(f'/Servicio/Actualizar/{id}')
        
            # Verificar que el número mínimo no sea negativo
            min_personas = request.POST.get('min_personas')
            if int(min_personas) < 0:
                messages.error(request, 'El número mínimo de personas no puede ser negativo.')
                return redirect(f'/Servicio/Actualizar/{id}')
        
            # Verificar que el número máximo no sea negativo
            max_personas = request.POST.get('max_personas')
            if int(max_personas) < 0:
                messages.error(request, 'El número máximo de personas no puede ser negativo.')
                return redirect(f'/Servicio/Actualizar/{id}')
        
            # Verificar que el número mínimo no sea mayor que el número máximo
            if int(min_personas) > int(max_personas):
                messages.error(request, 'El número mínimo de personas no puede ser mayor que el número máximo de personas.')
                return redirect(f'/Servicio/Actualizar/{id}')
            
            # Continuar con el procesamiento si la extensión y la longitud de la descripción son válidas
            servicio.nombre = request.POST.get('nombre')
            # Asignar el nombre único a la imagen
            img.name = f'Service_img_{id}.{ext}'
            servicio.foto = img
            servicio.descripcion = descripcion
            servicio.precio = request.POST.get('precio')
            servicio.categoria = request.POST.get('categoria')
            estado = request.POST.get('estado')
            estado = True if estado == 'True' else False
            servicio.estado = estado
            dias_dispo = '-'.join(request.POST.getlist('dias_dispo'))
            servicio.dias_dispo = dias_dispo
            servicio.max_personas = request.POST.get('max_personas')
            servicio.min_personas = request.POST.get('min_personas')
            
            servicio.save()
            
            return redirect('/Servicios/Index')
        else:
            messages.error(request, 'Por favor, complete todos los campos.')
            return redirect(f'/Servicio/Actualizar/{id}')
    else:
        servicio = Servicio.objects.filter(id=id)
        return render(request, 'Servicios/ActualizarServicio.html', {'servicio': servicio})
    
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

def View_Login(request):
    if request.method == "POST":
        if request.POST.get('username') and request.POST.get('password'):
            user = authenticate(username=request.POST.get('username'), password=request.POST.get('password'))
            if user is not None:
                login(request, user)
                return redirect("/Index/Home")
            else:
                messages.error(request, 'Credenciales de inicio de sesión incorrectas')
                return redirect('/Login/IniciarSesion')
    else:
        return render(request, 'Login/Login.html')
    
def LogoutUser(request):
    logout(request)
    return redirect('/Login/IniciarSesion')

#endregion

#region Usuario

def Crear_Usuario(request):
    if request.method == 'POST':
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        
        if password and confirm_password and email and first_name and last_name:
            if password == confirm_password:
                # Verificar la longitud de la contraseña
                if len(password) >= 8:
                    # Verificar si la contraseña contiene una letra mayúscula y un número utilizando una expresión regular
                    if re.search(r'^(?=.*[A-Z])(?=.*\d)', password):
                        # Verificar si el email ya existe en la base de datos
                        if User.objects.filter(email=email).exists():
                            messages.error(request, 'El email ya está registrado')
                            return redirect('/Login/CrearUser')
                        # Verificar si el usuario ya existe en la base de datos
                        if User.objects.filter(username=email).exists():
                            messages.error(request, 'El usuario ya existe')
                            return redirect('/Login/CrearUser')
                        usuario = User.objects.create_user(username=email, email=email, password=password, first_name=first_name, last_name=last_name)
                        usuario.save()
                        # Obtener el ID del usuario recién creado
                        id = usuario.id
                        profile = Profile.objects.create(id=id, auth_user_id=id)
                        profile.save()
                        # Iniciar sesión automáticamente en el usuario creado
                        user = authenticate(request, username=email, password=password)
                        if user is not None:
                            login(request, user)
                        # Obtener el ID del usuario recién creado
                        id = usuario.id
                        return redirect(f'/Usuario/Perfil/{id}')
                    else:
                        # La contraseña no contiene una letra mayúscula y un número
                        messages.error(request, 'La contraseña debe contener al menos una letra mayúscula y un número')
                        return redirect('/Login/CrearUser')
                else:
                    # La contraseña no tiene al menos 8 caracteres
                    messages.error(request, 'La contraseña debe tener al menos 8 caracteres')
                    return redirect('/Login/CrearUser')
            else:
                # Las contraseñas no son iguales
                messages.error(request, 'Las contraseñas no coinciden')
                return redirect('/Login/CrearUser')
        else:
            # Faltan campos obligatorios
            messages.error(request, 'Faltan campos obligatorios')
            return redirect('/Login/CrearUser')
    else:
        return render(request, 'Login/CrearUsuario.html')

def Listado_Usuarios (request):
    busqueda = request.GET.get('buscar')
    usuario = User.objects.all()
    profile = Profile.objects.all()

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

    context = { 'usuario':usuario,'current_page':current_page,'paginas':paginas,'profile':profile}
    

    return render(request,'Usuarios/ListadoUsuarios.html',context)

def Actualizar_Usuarios(request, id):
    if request.method == 'POST':
        perfil_img = request.FILES.get('profile_img')
        telefono = request.POST.get('telefono')
        documento = request.POST.get('documento')

        # Verificar el formato de la imagen
        if perfil_img.name.split(".")[-1].lower() not in ['jpeg', 'jpg', 'png']:
            messages.error(request, 'Formato de imagen no válido. Por favor, seleccione una imagen en formato JPEG, PNG o JPG.')
            return redirect(f'/Usuario/Actualizar/{id}')
        
        if perfil_img and telefono and documento:
            perfil = Profile.objects.get(id=id)

            # Verificar si la imagen existe
            if perfil.profile_img:
                ruta_foto = "media/" + str(perfil.profile_img)
                
                # Eliminar la imagen existente
                if os.path.exists(ruta_foto):
                    os.remove(ruta_foto)

            perfil.profile_img = perfil_img
            perfil.profile_img.name = f'Profile_img_{id}.{perfil.profile_img.name.split(".")[-1]}'
            perfil.telefono = telefono
            perfil.documento = documento
            perfil.save()
        
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        
        if first_name and last_name and email:
            usuario = User.objects.get(id=id)
            usuario.first_name = first_name
            usuario.last_name = last_name
            usuario.email = email
            usuario.username = email
            usuario.save()
        
        return redirect('/Usuarios/ListadoUser')
    else:
        perfil = Profile.objects.filter(id=id)
        return render(request, 'Usuarios/ActualizarUsuarios.html', {'perfil': perfil})
    
def Perfil_Usuarios (request,id):

    if request.method == 'POST':
        telefono = request.POST.get('telefono')
        documento = request.POST.get('documento')
        profile_img = request.FILES['profile_img']

        # Verificar el formato de la imagen
        if profile_img.name.split(".")[-1].lower() not in ['jpeg', 'jpg', 'png']:
            messages.error(request, 'Formato de imagen no válido. Por favor, seleccione una imagen en formato JPEG, PNG o JPG.')
            return redirect(f'/Usuario/Perfil/{id}')
            
        # Obtener el usuario actual
        usuario = request.user
        id = usuario.id

        # Generar un nombre de archivo único para la imagen
        profile_img.name = f'Profile_img_{id}.{profile_img.name.split(".")[-1]}'

        # Crear un nuevo objeto Profile con los datos del formulario
        profile = Profile(id=id, telefono=telefono, documento=documento, profile_img=profile_img, auth_user=usuario)

        profile.save()

        return redirect ('/Index/Home')
    else:
        usuario = User.objects.filter(id=id)
        return render (request, 'Usuarios/CompletarPerfil.html', {'usuario':usuario})

def Eliminar_Usuario (request, id):

    perfil = Profile.objects.get(id=id)
    perfil.delete()

    usuario = User.objects.get(id=id)
    usuario.delete()
    
    return redirect('/Usuarios/ListadoUser')

def Estado_Usuario(request, id):
    usuario = User.objects.get(id=id)

    # Cambiar el estado actual al estado opuesto
    usuario.is_active = not usuario.is_active

    usuario.save()

    return redirect('/Usuarios/ListadoUser')

def Usuario_admin(request, id):
    usuario = User.objects.get(id=id)

    # Cambiar el estado actual al estado opuesto
    usuario.is_superuser = not usuario.is_superuser

    usuario.save()

    return redirect('/Usuarios/ListadoUser')
#endregion

#region Reservas

def Reserva_Servicio(request, id):
    servicio = get_object_or_404(Servicio, id=id)
    usuario = request.user
    if request.method == 'POST':
        fecha_inicio = request.POST.get('fecha_inicio')
        fecha_final = request.POST.get('fecha_final')
        telefono = request.POST.get('telefono')
        documento = request.POST.get('documento')

        if fecha_inicio and fecha_final and telefono and documento:
            reserva = Reserva()
            reserva.usuario = usuario
            reserva.servicio = servicio
            reserva.fecha_inicio = request.POST.get('fecha_inicio') 
            reserva.fecha_final = request.POST.get('fecha_final')
            reserva.estado = True
            reserva.telefono = telefono
            reserva.documento = request.POST.get('documento')
            reserva.save()
            return redirect('/Servicios/Index')

    context = {'servicio': servicio}
    return render(request, 'Reservas/ReservarServicio.html', context)

def Listado_Reservas (request):

    reserva = Reserva.objects.all()

    busqueda = request.GET.get('buscar')
    if busqueda:
        reserva = Reserva.objects.filter(
            Q(documento__icontains = busqueda) 
        ).distinct()

    paginador = Paginator(reserva,10)
    pagina = request.GET.get('page') or 1
    reserva = paginador.get_page(pagina)
    current_page = int(pagina)
    paginas = range(1, reserva.paginator.num_pages + 1)
    
    context = {'reservas':reserva,'current_page':current_page,'paginas':paginas}

    return render(request,'Reservas/ListadoReservas.html', context)

def Estado_Reserva(request, id):

    reserva = Reserva.objects.get(id=id)

    # Cambiar el estado actual al estado opuesto
    reserva.estado = not reserva.estado

    reserva.save()

    return redirect ('/Reservas/ListadoReservas')

def Reservas_Usuario (request):

    reservas = Reserva.objects.all()

    context = {'reservas':reservas}

    return render(request,'Reservas/ReservasUsuario.html',context)
#endregion

# region restaurantes

def View_Restaurantes (request):

    restaurantes = Restaurante.objects.all()

    cantidad_restaurantes = Restaurante.objects.count()

    context = {'restaurantes':restaurantes,
               'cantidad_restaurantes': cantidad_restaurantes}


    return render (request,'Restaurantes/Index.html', context)

def Agregar_Restaurante(request):
    if request.method == 'POST':
        if request.POST.get('name') and request.FILES['url_img'] and request.POST.get('descripcion') and request.POST.get('ubicacion') and request.POST.get('estado'):
            restaurante = Restaurante()
            restaurante.name = request.POST.get('name')
            restaurante.url_img = request.FILES['url_img']
            restaurante.descripcion = request.POST.get('descripcion')
            restaurante.ubicacion = request.POST.get('ubicacion')
            estado = request.POST.get('is_active')
            estado = True if estado == 'False' else False
            restaurante.is_active = estado
            restaurante.save()  # Guarda el restaurante en la base de datos

            return redirect('/Restaurantes/Index')
    return render(request, 'Restaurantes/AgregarRestaurantes.html')

def Listado_Restaurantes (request):

    busqueda = request.GET.get('buscar')

    restaurante = Restaurante.objects.all()

    if busqueda:
        restaurante = Restaurante.objects.filter(
            Q(name__icontains = busqueda)
        ).distinct()

    paginador = Paginator(restaurante,5)
    pagina = request.GET.get('page') or 1
    restaurante = paginador.get_page(pagina)
    current_page = int(pagina)

    paginas = range(1, restaurante.paginator.num_pages + 1)

    context = { 'restaurantes':restaurante,'current_page':current_page,'paginas':paginas}
    
    return render(request,'Restaurantes/ListadoRestaurantes.html',context)
#endregion

#region Habitaciones

def View_Habitaciones (request):

    return render (request, 'Habitaciones/Index.html')

def Agregar_Habitacion (request):

    return render (request, 'Habitaciones/AgregarHabitacion.html')

#endregion