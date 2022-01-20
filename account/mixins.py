from django.http import Http404
from django.shortcuts import get_object_or_404,redirect
from blog.models import Article
from django.contrib.auth.mixins import LoginRequiredMixin

class FieldMixin():

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_superuser:
            self.fields = ['author','title','slug','category','description','thumbnail','is_special','status']
        elif request.user.is_author:
            self.fields = ['title','slug','category','description','is_special','thumbnail']
        else:
            raise Http404
        return super().dispatch(request, *args, **kwargs)


class FormValidMixin():
    def form_valid(self,form):
        if self.request.user.is_superuser:
            form.save()
        else:
            self.obj = form.save(commit=False)
            self.obj.author = self.request.user
            self.obj.status = 'd'
        return super().form_valid(form)

class AuthorAccessMixin():

    def dispatch(self, request,pk ,*args, **kwargs):
        article =get_object_or_404(Article,pk=pk)
        if article.author == request.user and article.status == 'd' or request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        else:
            raise Http404





class SuperUserMixin():

    def dispatch(self, request ,*args, **kwargs):

        if  request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        else:
            raise Http404
class AuthorsMixin():

    def dispatch(self, request ,*args, **kwargs):
        if request.user.is_authenticated or request.user.is_author:
            if  request.user.is_superuser or request.user.is_author:
                return super().dispatch(request, *args, **kwargs)
            else:
                return redirect("account:profile")
        else:
            return redirect('login')


