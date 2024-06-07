from django.urls import path
from . import views


app_name = 'blog' 
urlpatterns = [
    path('', views.PostListaView.as_view(), name='post_lista'), # Esta es la vista basada en clases
    #path('', views.post_lista, name='post_lista'), # Esta es la vista basada en funciones
    path('<int:year>/<int:month>/<int:day>/<slug:post>/',views.post_detalle,name='post_detalle'),
    path('<int:post_id>/compartir/',views.post_compartir, name='post_compartir'),
    path('<int:post_id>/comentar/',views.post_comentar, name='post_comentar'),
]