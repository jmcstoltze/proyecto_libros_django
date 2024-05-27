from .models import Genero, Libro, Autor, Resena
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from math import ceil

'''
    En virtud del plazo, se completan los métodos más urgentes relacionados con la "primera entrega",
    con la intención de completarla si es que el tiempo alcanza y/o en la medidad que estos métodos vayan siendo utilizados efectivamente
    en las vistas.

'''

### CREATE ###############################
# Crea libro (destinado para agregar libros por parte de el o los administradores del sitio)
def crear_libro(titulo, descripcion, anio_publicacion, generos_ids=None, autores_ids=None, portada_url=None):
    """
    Crea un nuevo registro de libro.

    :param titulo: Título del libro
    :param descripcion: Descripción del libro
    :param anio_publicacion: Año de publicación del libro
    :param generos_ids: Lista de IDs de géneros (opcional)
    :param autores_ids: Lista de IDs de autores (opcional)
    :param portada_url: URL de la portada del libro (opcional)
    :return: El objeto libro creado
    """
    
    # Si estos parámetros vienen vacíos
    if generos_ids is None:
        generos_ids = []
    if autores_ids is None:
        autores_ids = []

    # Crea el libro
    libro = Libro.objects.create(
        titulo=titulo,
        descripcion=descripcion,
        anio_publicacion=anio_publicacion,
        portada_url=portada_url if portada_url else "" # Si no hay str de portada se deja en blanco
    )

    # Asigna géneros
    for genero_id in generos_ids:
        genero = Genero.objects.get(id=genero_id)
        libro.genero.add(genero)

    # Asignar autores
    for autor_id in autores_ids:
        autor = Autor.objects.get(id=autor_id)
        libro.autor.add(autor)

    # Guarda el libro con los géneros y autores
    libro.save()

    return libro


# Crea usuario empleando el usuario por defecto de Django
def crear_usuario(email, password, first_name, last_name):
    """
    Crea un nuevo usuario utilizando el modelo de usuario por defecto de Django.

    :param email: Correo electrónico del usuario
    :param password: Contraseña del usuario
    :param first_name: Nombre del usuario
    :param last_name: Apellido del usuario
    :return: El objeto usuario creado
    """
    # Asigna automáticamente el nombre de usuario como "usuario" + ID, ya que el modelo presentado en los requerimientos no incluye username
    username = f"usuario{User.objects.count() + 1}"
    
    # Crea el usuario
    usuario = User.objects.create_user(
        username=username,
        email=email,
        password=password,
        first_name=first_name,
        last_name=last_name
    )
    
    return usuario


# Crea reseña ingresada por usuario
def crear_resena(libro, usuario, calificacion, comentario):
    """
    Crea una nueva reseña para un libro.

    :param libro: Instancia del libro para el cual se está creando la reseña
    :param usuario: Usuario que está creando la reseña
    :param calificacion: Calificación asignada a la reseña
    :param comentario: Comentario asociado a la reseña
    :return: El objeto de la reseña creada
    """

    # Crea el objeto reseña con los parámetros y lo retorna
    nueva_resena = Resena.objects.create(
        libro=libro,
        usuario=usuario,
        calificacion=calificacion,
        comentario=comentario
    )
    return nueva_resena


def crear_autor(nombre, apellido):
    """
    Crea un nuevo autor si no existe.

    :param nombre: Nombre del autor
    :param apellido: Apellido del autor
    :return: El objeto Autor creado o el existente
    """

    # Verifica y/o crea el objeto autor con los parámetros y lo retorna
    autor, creado = Autor.objects.get_or_create(
        nombre=nombre,
        apellido=apellido
    )
    return autor

### READ ###############################
# Obtener todos los libros
def obtener_libros():
    """
    Obtiene todos los libros de la base de datos.

    :return: QuerySet de todos los libros
    """
    libros = Libro.objects.all()

    # Retorna todos los libros
    return libros


# Obtiene un libro por su ID
def obtener_libro_por_id(libro_id):
    """
    Obtiene un libro específico por su ID.

    :param libro_id: ID del libro a obtener
    :return: Instancia del libro
    """
    
    # Retorna el libro
    libro = Libro.objects.get(id=libro_id)
    return libro


# Obtiene los libros de un autor
def obtener_libros_por_autor(id_autor):
    """
    Obtiene los libros escritos por un autor específico.

    :param id_autor: ID del autor
    :return: QuerySet de libros escritos por el autor dado
    """
    # Retorna los libros del autor con el ID proporcionado
    libros_por_autor = Libro.objects.filter(autor__id=id_autor)
    return libros_por_autor


def obtener_calificacion_libro(libro_id):
    """
    Obtiene el promedio de calificación de un libro específico.

    :param libro_id: ID del libro
    :return: Promedio de calificación del libro
    """
    # Obtien las reseñas del libro
    resenas = Resena.objects.filter(libro_id=libro_id)
    
    # Calcula el promedio de calificaciones
    if resenas.exists():
        total_calificaciones = sum([resena.calificacion for resena in resenas])
        promedio_calificacion = total_calificaciones / resenas.count()
        # Redondea hacia arriba el valor
        promedio_calificacion = ceil(promedio_calificacion)
        return promedio_calificacion
    else:
        return None # Si el libro no ha sido calificado


# Obtiene los libros de una categoría en particular 
def obtener_libros_por_categoria(categoria):
    """
    Obtiene todos los libros que pertenecen a una categoría específica.

    :param categoria: Categoría por la cual filtrar los libros.
    :return: QuerySet de libros que pertenecen a la categoría especificada.
    """
    # Retorna todos los libros filtrados por catgoría
    libros = Libro.objects.filter(genero=categoria)
    return libros


# Obtiene los libros de una determinada calificación
def obtener_libros_por_calificacion(calificacion):
    """
    Obtiene todos los libros que tienen una calificación específica.

    :param calificacion: Calificación por la cual filtrar los libros.
    :return: QuerySet de libros que tienen la calificación especificada.
    """
    libros_calificacion = [] # Almacenará los libros solicitados
    libros = obtener_libros()

    # Itera todos los libros
    for libro in libros:
        # Obtiene todas la calificaciones del libro iterado
        calificaciones = libro.resena_set.values_list('calificacion', flat=True)
        # Si tiene calificaciones calcula el promedio de calificación aproximando hacia arriba
        if calificaciones:
            promedio_calificacion = ceil(sum(calificaciones) / len(calificaciones))
            
            # Si el promedio coincide con el criterio de búsqueda el libro se agrega al retorno
            if promedio_calificacion == calificacion:
                libros_calificacion.append(libro)

    # Retorna los libros buscados
    return libros_calificacion


# Método para obtener el usuario mediante el email
def obtener_usuario(email):
    """
    Obtiene un usuario por su dirección de correo electrónico

    :param email: Dirección de correo electrónico del usuario
    :return: Objeto de usuario
    """
    # Autenticar el usuario
    user = User.objects.get(email=email)

    # Retorna usuario o None
    return user


def obtener_autores():
    """
    Obtiene todos los autores

    :param : None
    :return: Todos los Objetos de autor
    """
    # Obtiene todos los autores y los retorna
    autores = Autor.objects.all()
    return autores


def obtener_autor_por_id(autor_id):
    """
    Obtiene un autor por su ID.

    :param autor_id: ID del autor
    :return: Objeto del autor
    """
    # Retorna el autor
    autor = Autor.objects.get(id=autor_id)
    return autor


def obtener_generos():
    """
    Obtiene todos los géneros o categorías

    :param : None
    :return: Todos los Objetos de género
    """
    # Obtiene todos los géneros y los retorna
    generos = Genero.objects.all()
    return generos


# Método para obtener las reseñas de un libro
def obtener_resenas(libro):
    """
    Obtiene todas las reseñas asociadas a un libro dado.

    :param libro: El libro del cual se quieren obtener las reseñas.
    :return: Una lista de instancias de Resena asociadas al libro.
    """
    # Utiliza la relación inversa para obtener las reseñas del libro dado
    return libro.resena_set.all()


'''
    Se reitera la idea de que, en virtud del plazo, se completan los métodos más urgentes relacionados con la "primera entrega",
    con la intención de completarla si es que el tiempo alcanza y/o en la medidad que estos métodos vayan siendo utilizados efectivamente
    en las vistas.

'''