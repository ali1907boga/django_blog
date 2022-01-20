from django.urls import path,include
from .views import ArticleList,ArticleDetail,ArticleDelete,UserList,UserDetail

app_name = 'api'

urlpatterns = [

    path('api/',ArticleList.as_view(),name='article_list'),
    path('<slug:slug>/',ArticleDetail.as_view(),name='detail'),
    path('Delete/<int:pk>/',ArticleDelete.as_view(),name='delete'),
    path('users/',UserList.as_view(),'user_list'),
    path('users/<int:pk>/',UserDetail.as_view(),name='user_detail'),


]