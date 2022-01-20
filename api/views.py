from django.shortcuts import render
from django.views.generic import ListView
from rest_framework.generics import ListAPIView,RetrieveAPIView,DestroyAPIView,RetrieveDestroyAPIView,RetrieveUpdateAPIView
from .permissions import IsSuperUser,IsStaffOrReadOnly,IsAuthorOrReadOnly,IsSuperUserOrStaffReadOnly
from blog.models import Article,User
from .serializers import ArticleSerializer,UserSerializer

class ArticleList(ListAPIView):
    queryset = Article.objects.published()
    serializer_class = ArticleSerializer


class ArticleDetail(RetrieveUpdateAPIView):
    queryset = Article.objects.published()
    serializer_class = ArticleSerializer
    permission_classes = [IsStaffOrReadOnly,IsAuthorOrReadOnly]
    lookup_field = 'slug'


class ArticleDelete(RetrieveUpdateAPIView):
    queryset = Article.objects.published()
    serializer_class = ArticleSerializer

class UserList(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsSuperUserOrStaffReadOnly,)

class UserDetail(RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsSuperUser,)


# Create your views here.
