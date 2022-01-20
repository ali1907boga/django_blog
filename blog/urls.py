from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [

    path ('',views.Article_List.as_view(),name = 'home'),
    path('page/<int:page>',views.Article_List.as_view(),name='home'),
    path('<slug:slug>/',views.Article_Detail.as_view(),name='detail'),
    path('preview/<int:pk>/',views.Article_Preview.as_view(),name='preview'),
    path('category/<slug:slug>/',views.Category_List.as_view(),name='category'),
    path('author/<slug:username>/',views.Author_List.as_view(),name='author'),
    path('search/',views.Search_List.as_view(),name='search'),
    path('search/page/<int:page>',views.Search_List.as_view(),name='search'),




]
