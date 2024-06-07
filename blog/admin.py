from django.contrib import admin
from .models import Post, Comentario

# Registra el modelo Post en el panel de administración de Django. 
# admin.site.register(Post) . 

# Otra forma de registrar el modelo Post en el panel de administración de Django de manera más personalizada.
@admin.register(Post) 
class PostAdmin(admin.ModelAdmin): 
    list_display = ['titulo', 'slug', 'autor', 'fecha_publicado', 'estado'] # Muestra los campos titulo, slug, autor, fecha_publicado y estado en la lista de objetos.
    list_filter = ['estado', 'fecha_creado', 'fecha_publicado', 'autor'] # Agrega un panel de filtro en el lado derecho de la página que permite filtrar los resultados por los campos estado, fecha_creado, fecha_publicado y autor.
    search_fields = ['titulo', 'cuerpo'] # Agrega un campo de búsqueda en la parte superior de la página que permite buscar objetos por los campos titulo y cuerpo.
    prepopulated_fields = {'slug': ('titulo',)} # Crea un campo de slug que se rellena automáticamente con el valor del campo titulo.
    ordering = ['estado', 'fecha_publicado'] # Ordena los objetos por los campos estado y fecha_publicado en orden ascendente.

@admin.register(Comentario) 
class ComentarioAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'email', 'post', 'fecha_creado', 'activo']
    list_filter = ['activo', 'fecha_creado']
    search_fields = ['nombre', 'email', 'cuerpo']
