from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse


class Post(models.Model):
    class Estado(models.TextChoices): # Enumeración de opciones de estado : Borrador y Publicado
        BORRADOR = 'BR', 'Borrador'
        PUBLICADO = 'PB', 'Publicado'
    
    titulo = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250)
    autor = models.ForeignKey(User,
                               on_delete=models.CASCADE)
    cuerpo = models.TextField()
    fecha_publicado = models.DateTimeField(default=timezone.now)
    fecha_creado = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=2,
                              choices=Estado.choices,
                              default=Estado.BORRADOR)

    def __str__(self):
        return self.titulo
    
    #IMPORTANTE : Esta funcion devuelve la URL canónica de un post.
    def get_absolute_url(self): # reverse() genera la URL absoluta a partir de la vista y los parámetros dados.
        return reverse('blog:post_detalle',
                       args=[self.fecha_publicado.year,
                            self.fecha_publicado.month,
                            self.fecha_publicado.day,
                            self.slug])



class Comentario(models.Model):
    post = models.ForeignKey(Post,
                             on_delete=models.CASCADE,
                             related_name='comentarios') # Relación inversa para acceder a los comentarios de un post.
    nombre = models.CharField(max_length=80)
    email = models.EmailField()
    cuerpo = models.TextField()
    fecha_creado = models.DateTimeField(auto_now_add=True)
    activo = models.BooleanField(default=True)
    
    def __str__(self):
        return f'Comentario por {self.nombre} en {self.post}'