from django.contrib.auth import views
from django.urls import path
from .views import home
from .views import ArticleList,ArticleCreate,ArticleUpdate,ArticleDelete,Profile

app_name = 'account'



urlpatterns = [

    path('home/',ArticleList.as_view(),name='home'),
    path('article/create/',ArticleCreate.as_view(),name='article_create_update'),
    path('article/update/<int:pk>/',ArticleUpdate.as_view(),name= 'article_update'),
    path('article/delete/<int:pk>/',ArticleDelete.as_view(),name='article_delete'),
    path('article/profile/',Profile.as_view(),name='profile'),

]