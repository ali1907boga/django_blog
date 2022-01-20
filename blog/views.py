
from django.shortcuts import render,get_object_or_404
from django.views.generic import ListView, DetailView
from account.models import User
from .models import Article,Category,ArticleHit,IPAddress
from account.mixins import AuthorAccessMixin
from django.core.paginator import Paginator

# Create your views here.


#def article_list(request):
    #articles_list = Article.objects.published()
    #paginator = Paginator(articles_list,1)
    #page = request.GET.get('page')
    #articles = paginator.get_page(page)
    #category = Category.objects.filter(status=True)
    #return render(request,'home.html',{'articles':articles,'category':category})






class Article_List(ListView):

    queryset = Article.objects.published()
    paginate_by = 4
    template_name = 'home.html'
    #context_object_name = 'articles'


#def detail(request,slug):
   # article = get_object_or_404(Article,slug=slug)
   # return render(request,'detail.html',{'article':article})


class Article_Detail(DetailView):
    template_name = 'detail.html'
    def get_object(self):
        slug = self.kwargs.get('slug')
        article =  get_object_or_404(Article.objects.published(),slug=slug)
        ip_address = self.request.user.ip_address
        if ip_address not in article.hits.all() :

            article.hits.add(ip_address)


        return article



class Article_Preview(AuthorAccessMixin,DetailView):
    template_name = 'detail.html'
    def get_object(self):
        pk = self.kwargs.get('pk')
        return get_object_or_404(Article,pk=pk)






#def category(request,slug):
    #category = get_object_or_404(Category,slug = slug,status= True)
    #article_list = category.articles.published()
    #paginator = Paginator(article_list)
    #page = request.GET.get('page')
    #articles = paginator.get_page(page)
#def author(request,username):
    #author = get_object_or_404(User,username=username)
    #article_list = author.articles.published()
    #paginator = Paginator(article_list)
    #page = request.GET.get('page')
    #articles = paginator.get_page(page)
    #return render(request,'author_list.html',{'author':author,'articles':articles})



class Category_List(ListView):
    paginate_by = 1
    template_name = 'category.html'
    def get_queryset(self):
        global category
        slug = self.kwargs.get('slug')
        category = get_object_or_404(Category.objects.active(),slug=slug)
        return category.articles.published()
    def get_context_data(self, *, object_list=None, **kwargs):
        slug = self.kwargs.get('slug')
        context = super().get_context_data(**kwargs)
        context['category'] = category
        return context

class Author_List(ListView):
    paginate_by = 1
    template_name = 'author_list.html'
    def get_queryset(self):
        global author
        username = self.kwargs.get('username')
        author = get_object_or_404(User,username=username)
        return author.articles.published()
    def get_context_data(self, *, object_list=None, **kwargs):
        slug = self.kwargs.get('slug')
        context = super().get_context_data(**kwargs)
        context['author'] = author
        return context


class Search_List(ListView):
    paginate_by = 1
    template_name = 'search_list.html'
    def get_queryset(self):
        search = self.request.GET.get('q')
        return Article.objects.filter(description__icontains=search)
    def get_context_data(self, *, object_list=None, **kwargs):

        context = super().get_context_data(**kwargs)
        context['search'] = self.request.GET.get('q')




