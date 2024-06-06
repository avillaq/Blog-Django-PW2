from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

# Manager personalizado . Un manager es un objeto que maneja consultas a la base de datos.
class PublishedManager(models.Manager):
    def get_queryset(self):
        # Este método filtra los objetos de la base de datos para que solo se devuelvan los  que tienen el estado publicado.
        return super().get_queryset()\
                     .filter(status=Post.Estado.PUBLICADO) 

class Post(models.Model):
    class Estado(models.TextChoices): # Enumeración de opciones de estado : Borrador y Publicado
        BORRADOR = 'BR', 'Borrador'
        PUBLICADO = 'PB', 'Publicado'
    
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250,
                            unique_for_date='publish')
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='blog_posts')
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=2,
                              choices=Estado.choices,
                              default=Estado.BORRADOR)
    
    # Managers (Opcional)
    published = PublishedManager() # Este manager se puede usar para recuperar todos los objetos Post que tienen el estado publicado.


    class Meta:
        ordering = ['-publish'] # Cuando se consulte la base de datos, los resultados se ordenarán por el campo publish en orden descendente.


    def __str__(self):
        return self.title
    
    #IMPORTANT This method will return the canonical URL for a post
    def get_absolute_url(self):
        return reverse('blog:post_detail',
                       args=[self.publish.year,
                            self.publish.month,
                            self.publish.day,
                            self.slug])



class Comment(models.Model):
    post = models.ForeignKey(Post,
                             on_delete=models.CASCADE,
                             related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    class Meta:
        ordering = ['created']
        indexes = [
            models.Index(fields=['created']),
        ]
    def __str__(self):
        return f'Comment by {self.name} on {self.post}'