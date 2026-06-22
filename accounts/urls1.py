from django.urls import path
from .views import  PostUpdate, ArticleCreate, PostDelete

urlpatterns = [
   path('create/', ArticleCreate.as_view(), name='article_create'),
   path('<int:pk>/update/', PostUpdate.as_view(), name='post_update'),
   path('<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),


]