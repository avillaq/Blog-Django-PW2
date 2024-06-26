from django.shortcuts import render, get_object_or_404
from .models import Post

# Pagination
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Email form
from .forms import ComentarioForm
from django.core.mail import send_mail
from django.views.decorators.http import require_POST
from django.views.generic import ListView


#IMPORTANTE: Vista basada en clases que muestra una lista de publicaciones.
class PostListaView(ListView): # Hereda de la clase ListView que es una vista genérica que se utiliza para mostrar una lista de objetos.
    # Esta vista es una alternativa a la vista basada en funciones post_list.

    # Obtiene todos los objetos Post que tienen el estado publicado y los ordena por fecha de publicación en orden descendente.
    queryset = Post.objects.filter(estado=Post.Estado.PUBLICADO).order_by('-fecha_publicado')
    context_object_name = 'posts' # El nombre de la variable de contexto que se utilizará en la plantilla.
    paginate_by = 3 # Muestra 3 posts por página.
    template_name = 'blog/post/lista.html' # La plantilla que se utilizará para renderizar la página.


def post_lista(request):
    # Obtiene todos los objetos Post que tienen el estado publicado y los ordena por fecha de publicación en orden descendente.
    posts = Post.objects.filter(estado=Post.Estado.PUBLICADO).order_by('-fecha_publicado')  
    
    # Paginator mostrara 3 posts por página
    paginador = Paginator(posts, 3)
    numero_pagina = request.GET.get('page', 1) # Obtiene el número de página de la URL de la solicitud.
    try:
        posts = paginador.page(numero_pagina)
    except PageNotAnInteger:
        # Si numero_pagina no es un entero, devuelve la primera página de resultados
        posts = paginador.page(1)
    except EmptyPage:
        # Si numero_pagina es un entero pero no hay resultados, devuelve la última página de resultados
        posts = paginador.page(paginador.num_pages)

    return render(request,
                'blog/post/lista.html',
                {'posts': posts})

def post_detalle(request, year, month, day, post):
    # get_object_or_404 es una función que recupera un objeto de la base de datos o devuelve un error 404 si el objeto no existe.
    post = get_object_or_404(Post,
                            estado=Post.Estado.PUBLICADO,
                            slug=post,
                            fecha_publicado__year=year,
                            fecha_publicado__month=month,
                            fecha_publicado__day=day)
    
    # Lista de comentarios activos para este post
    comentarios = post.comentarios.filter(activo=True)
    # Formulario para comentar
    form = ComentarioForm()
    
    return render(request,
                  'blog/post/detalle.html',
                  {'post': post,
                   'comentarios': comentarios,
                   'form': form})

@require_POST # Decorador que permite que la vista solo se pueda acceder a través de una solicitud POST.
def post_comentar(request, post_id):
    post = get_object_or_404(Post, id=post_id, estado=Post.Estado.PUBLICADO)
    comentario = None  # Varialbe que almacena el comentario e indica si el comentario se ha guardado correctamente. 
    form = ComentarioForm(data=request.POST)
    if form.is_valid():
        # Crea un objeto Comment pero no lo guarda en la base de datos todavía.
        comentario = form.save(commit=False)
        # Asigna el post actual al comentario
        comentario.post = post
        # Guarda el comentario en la base de datos
        comentario.save()
    return render(request, 'blog/post/comentario.html',
                           {'post': post,
                            'comentario': comentario})