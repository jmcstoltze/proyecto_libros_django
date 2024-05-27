from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect

from .models import Genero, Libro, Autor, Contacto
from datetime import datetime

from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import authenticate, login, logout

from .services import obtener_libros, obtener_libro_por_id, obtener_resenas, crear_resena, crear_usuario, obtener_usuario, obtener_autores, obtener_libros_por_autor, obtener_calificacion_libro, obtener_generos, obtener_libros_por_categoria, obtener_libros_por_calificacion, crear_autor, obtener_autor_por_id, crear_libro
# Create your views here.

def inicio(request):
    return render(request, "inicio.html", {})

def registro_usuario(request):

    if request.method == 'POST':
        # Obtiene los datos del formulario
        nombre = request.POST.get('nombre')
        apellidos = request.POST.get('apellidos')
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        # Crea un nuevo usuario utilizando services.py y redirige a la página de inicio
        crear_usuario(email, password, nombre, apellidos)
        return redirect('inicio')

    return render(request, "registro_usuario.html")  # Renderiza la página de registro

def iniciar_sesion(request):
    if request.method == 'POST':
        # Obtien los datos del formulario
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        usuario = obtener_usuario(email) # Obtiene el usuario

        # Autentica al usuario utilizando el username y la contraseña
        user = authenticate(request, username=usuario.username, password=password)
        
        # Si el usuario existe
        if user is not None:            
            login(request, user)
            return redirect('libros')  # Redirige a libros.html después del login
        else:
            # Si el usuario no existe o las credenciales son incorrectas se pasa un mensaje de error al contexto
            ######### NO SE HA IMPLEMENTADO EL MANEJO DE EXCEPCIONES ###################################
            return render(request, 'iniciar_sesion.html', {'error_message': 'Credenciales inválidas'})
    else:
        return render(request, 'iniciar_sesion.html', {})  # Renderiza la página
    
def cerrar_sesion(request):
    logout(request) # Solicitud de cierre de sesión
    return redirect('inicio')  # Redirige a la página de inicio


@login_required
def libros(request):
    libros = obtener_libros() # Llama a la función para obtener los libros
    return render(request, "libros.html", {'libros': libros}) # Renderiza y entrega el contexto


@login_required
def detalle_libro(request, libro_id):

    # Obtener el libro por su ID
    libro = obtener_libro_por_id(libro_id)
    resenas = obtener_resenas(libro) # Obtiene las reseñas del libro

    # Si se postea un nuevo comentario, toma la info desde el formulario
    if request.method == 'POST':
        comentario = request.POST.get('comentario')
        calificacion = request.POST.get('calificacion')

        # Crea una nueva reseña usando services.py
        crear_resena(libro, request.user, calificacion, comentario)

        # Redirecciona a la misma página para mostrar la nueva reseña
        return redirect('detalle_libro', libro_id=libro_id)
    
    return render(request, "detalle_libro.html", {
        'libro': libro,
        'resenas': resenas
    }) # Renderiza y entrega el contexto de la vista


@login_required
def busqueda(request):
    return render(request, "busqueda.html", {})


@login_required
def busqueda_autor(request):

    autores = obtener_autores() # Recopila todos los autores
    libros = [] # Inicializa lista de libros
    calificaciones = [] # Inicializa lista de calificaciones
    autor_id = None  # Inicializa la variable autor_id

    # Obtiene el autor seleccionado en el combobox de la vista
    if request.method == 'POST':
        autor_id = request.POST.get('autor_id')  # Obtener el ID del autor seleccionado
        # Obtener los libros asociados al autor seleccionado
        libros = obtener_libros_por_autor(autor_id)

        # Obtener la calificación de cada libro
        for libro in libros:
            calificacion = obtener_calificacion_libro(libro.id) # De services.py
            if calificacion is None:
                calificacion = "No ha sido calificado" # Si no hay calificación
            calificaciones.append((libro.id, calificacion))

    # Actualiza la lista de autores antes de devolver la respuesta
    autores = obtener_autores()
    return render(request, 'busqueda_autor.html', {'autores': autores, 'libros': libros, 'calificaciones': calificaciones})


@login_required
def busqueda_categoria(request):
    generos = obtener_generos() # Recopila todos los géneros
    libros = [] # Inicializa lista de libros
    calificaciones = [] # Inicializa lista de calificaciones
    categoria_id = None  # Inicializa la variable genero_id

    # Obtiene la categoría seleccionada en el combobox de la vista
    if request.method == 'POST':
        categoria_id = request.POST.get('categoria_id')  # Obtener el ID del género seleccionado
        # Obtener los libros asociados al autor seleccionado
        libros = obtener_libros_por_categoria(categoria_id)

        # Obtener la calificación de cada libro
        for libro in libros:
            calificacion = obtener_calificacion_libro(libro.id) # De services.py
            if calificacion is None:
                calificacion = "No ha sido calificado" # Si no hay calificación
            calificaciones.append((libro.id, calificacion))

    # Actualiza la lista de autores antes de devolver la respuesta
    generos = obtener_generos()
    return render(request, 'busqueda_categoria.html', {'generos': generos, 'libros': libros, 'calificaciones': calificaciones})


@login_required
def busqueda_calificacion(request):

    libros = [] # Inicializa lista de libros
    calificaciones = [] # Inicializa lista de calificaciones
    calificacion_solicitada = None  # Inicializa la variable calificacion solicitada
    
    # Obtiene el autor seleccionado en el combobox de la vista
    if request.method == 'POST':
        calificacion_solicitada = int(request.POST.get('calificacion_id')) # Almacena el valor de la búsqueda
        # Obtener los libros asociados a la calificación
        libros = obtener_libros_por_calificacion(calificacion_solicitada)

        # Obtener la calificación de cada libro
        for libro in libros:
            calificacion = obtener_calificacion_libro(libro.id) # De services.py
            if calificacion is None:
                calificacion = "No ha sido calificado" # Si no hay calificación
            calificaciones.append((libro.id, calificacion))

    return render(request, 'busqueda_calificacion.html', {'libros': libros, 'calificaciones': calificaciones})

# Verifica que usuario logeado es administrador superuser
def es_administrador(user):
    return user.is_authenticated and user.is_superuser

@user_passes_test(es_administrador)
def agregar_libro(request):

    generos = obtener_generos()
    autores = obtener_autores()
    anio_actual = datetime.now().year
    anios = range(anio_actual, 1000 - 1, -1) # Genera un rango de años para elegir

    if request.method == 'POST':
        titulo = request.POST.get('titulo')
        descripcion = request.POST.get('descripcion')
        anio_publicacion = int(request.POST.get('anio_publicacion'))
        url_imagen = request.POST.get('url_imagen') or 'img/imagen_no_disponible.jpg' # Imagen por defecto
        generos_ids = request.POST.get('genero')
        nombre_autor = request.POST.get('nombre_autor')
        apellido_autor = request.POST.get('apellido_autor')

        # Obtien o crea el autor
        autor, creado = Autor.objects.get_or_create(nombre=nombre_autor, apellido=apellido_autor)

        # Crea el libro con los datos proporcionados
        crear_libro(titulo, descripcion, anio_publicacion, generos_ids, [autor.id], url_imagen)

        return redirect('libros') # Retorna a la pagina de libros listados

    else:
        
        return render(request, "agregar_libro.html", {'generos': generos, 'anios': anios})


def contacto(request):
    if request.method == 'POST':
        # Obtiene los datos del formulario
        nombre = request.POST.get('nombre')
        apellidos = request.POST.get('apellidos')
        email = request.POST.get('email')
        mensaje = request.POST.get('mensaje')

        # Crea una instancia del modelo Contacto y guarda en la base de datos
        contacto = Contacto(nombre=nombre, apellido=apellidos, email=email, mensaje=mensaje)
        contacto.save()

        # Redirige a página de éxito
        return redirect('contacto_exitoso')

    # Renderiza la vista original
    return render(request, 'contacto.html')

def contacto_exitoso(request):
    return render(request, "contacto_exitoso.html", {})


'''  SE IMPLEMENTÓ OTRO TIPO DE LOGEO
class LoginRequiredMixin(View):

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

class Welcome(LoginRequiredMixin, TemplateView):
    template_name = "libros.html" '''