from django.contrib import admin
from .models import Post, Comment

# Registra el modelo Post en el panel de administración de Django. 
# admin.site.register(Post) . 

# Otra forma de registrar el modelo Post en el panel de administración de Django de manera más personalizada.
@admin.register(Post) 
class PostAdmin(admin.ModelAdmin): 
    list_display = ['title', 'slug', 'author', 'publish', 'status'] # Muestra los campos title, slug, author, publish y status en la lista de objetos.
    list_filter = ['status', 'created', 'publish', 'author'] # Agrega un panel de filtro en el lado derecho de la página que permite filtrar los resultados por los campos status, created, publish y author.
    search_fields = ['title', 'body'] # Agrega un campo de búsqueda en la parte superior de la página que permite buscar objetos por los campos title y body.
    prepopulated_fields = {'slug': ('title',)} # Crea un campo de slug que se rellena automáticamente con el valor del campo title.
    ordering = ['status', 'publish'] # Ordena los objetos por los campos status y publish en orden ascendente.

@admin.register(Comment) 
class CommentAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'post', 'created', 'active']
    list_filter = ['active', 'created', 'updated']
    search_fields = ['name', 'email', 'body']
