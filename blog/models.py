from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse


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
    status = models.CharField(max_length=2,
                              choices=Estado.choices,
                              default=Estado.BORRADOR)

    def __str__(self):
        return self.title
    
    #IMPORTANTE : Este método devuelve la URL canónica de un objeto.
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
    active = models.BooleanField(default=True)
    
    def __str__(self):
        return f'Comentario por {self.name} en {self.post}'