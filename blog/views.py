from django.shortcuts import render, get_object_or_404
from .models import Post, Comment

# Pagination
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Email form
from .forms import EmailPostForm, CommentForm
from django.core.mail import send_mail
from django.views.decorators.http import require_POST
from django.views.generic import ListView


#IMPORTANTE: Vista basada en clases que muestra una lista de publicaciones.
class PostListView(ListView): # Hereda de la clase ListView que es una vista genérica que se utiliza para mostrar una lista de objetos.
    # Esta vista es una alternativa a la vista basada en funciones post_list.

    queryset = Post.published.all()  # Obtiene todos los objetos Post que tienen el estado publicado.
    context_object_name = 'posts' # El nombre de la variable de contexto que se utilizará en la plantilla.
    paginate_by = 3 # Muestra 3 posts por página.
    template_name = 'blog/post/list.html' # La plantilla que se utilizará para renderizar la página.


def post_list(request):
    posts = Post.published.all() # Obtiene todos los objetos Post que tienen el estado publicado.
    
    # Paginator mostrara 3 posts por página
    paginator = Paginator(posts, 3)
    page_number = request.GET.get('page', 1) # Obtiene el número de página de la URL de la solicitud.
    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        # Si page_number no es un entero, devuelve la primera página de resultados
        posts = paginator.page(1)
    except EmptyPage:
        # Si page_number es un entero pero no hay resultados, devuelve la última página de resultados
        posts = paginator.page(paginator.num_pages)

    return render(request,
                'blog/post/list.html',
                {'posts': posts})

def post_detail(request, year, month, day, post):
    # get_object_or_404 es una función que recupera un objeto de la base de datos o devuelve un error 404 si el objeto no existe.
    post = get_object_or_404(Post,
                            status=Post.Status.PUBLISHED,
                            slug=post,
                            publish__year=year,
                            publish__month=month,
                            publish__day=day)
    
    # Lista de comentarios activos para esta publicación
    comments = post.comments.filter(active=True)
    # Formulario para comentar
    form = CommentForm()
    
    return render(request,
                  'blog/post/detail.html',
                  {'post': post,
                   'comments': comments,
                   'form': form})

def post_share(request, post_id):
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    sent = False # Variable que se establece en True si el correo electrónico se envía correctamente.

    if request.method == 'POST':
        # Form was submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # Form fields passed validation
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(
                    post.get_absolute_url())
            subject = f"{cd['name']} recommends you read " \
                        f"{post.title}"
            message = f"Read {post.title} at {post_url}\n\n" \
                        f"{cd['name']}\'s comments: {cd['comments']}"
            send_mail(subject, message, 'villafuertequispealex@gmail.com',
                        [cd['to']])
            sent = True
    else:
        form = EmailPostForm()
        
    return render(request, 'blog/post/share.html', {'post': post,
                                                    'form': form,
                                                    'sent': sent})

@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    comment = None
    # A comment was posted
    form = CommentForm(data=request.POST)
    if form.is_valid():
        # Create a Comment object without saving it to the database
        comment = form.save(commit=False)
        # Assign the post to the comment
        comment.post = post
        # Save the comment to the database
        comment.save()
    return render(request, 'blog/post/comment.html',
                           {'post': post,
                            'form': form,
                            'comment': comment})