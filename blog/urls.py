from django.urls import path
from . import views


app_name = 'blog' 
urlpatterns = [
    path('', views.PostListView.as_view(), name='post_list'), # Esta es la vista basada en clases
    #path('', views.post_list, name='post_list'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/',views.post_detail,name='post_detail'),
    path('<int:post_id>/share/',views.post_share, name='post_share'),
    path('<int:post_id>/comentario/',views.post_comentario, name='post_comentario'),
]