from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView,CreateView,UpdateView,DeleteView
from .mixins import FieldMixin,FormValidMixin,AuthorAccessMixin,SuperUserMixin,AuthorsMixin
from blog.models import Article
from .models import User
from django.urls import reverse_lazy
from .forms import ProfileForm
from django.contrib.auth.views import LoginView,PasswordChangeView



def home(request):
    return render(request,'registration/home.html')

class ArticleList(AuthorsMixin,ListView):
    def get_queryset(self):
        if self.request.user.is_superuser:
            return Article.objects.all()
        else:
            return Article.objects.filter(author=self.request.user)
    template_name = 'registration/home.html'

class ArticleList1(ListView):

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Article.objects.all()
        else:
            Article.objects.filter(author=self.request.user)



class ArticleCreate(AuthorsMixin,FormValidMixin,FieldMixin,CreateView):
    model = Article
    template_name = 'registration/article_create_update.html'
# Create your views here.
class ArticleUpdate(AuthorAccessMixin,FormValidMixin,FieldMixin,UpdateView):
    model = Article
    template_name = 'registration/article_create_update.html'

class ArticleDelete(SuperUserMixin ,DeleteView):
    model = Article
    success_url = reverse_lazy('account:home')
    template_name = 'registration/article_delete.html'

class Profile(LoginRequiredMixin,UpdateView):
    model = User

    template_name = 'registration/profile.html'
    form_class = ProfileForm
    success_url = reverse_lazy('account:profile')

    def get_object(self):
        return User.objects.get(pk = self.request.user.pk)



    def get_form_kwargs(self):
        kwargs = super(Profile,self).get_form_kwargs() #bayad an formi ke mikhahim user ya har etelati vared form shavad dakhel super benevisim.
        kwargs.update({
            'user': self.request.user
        })
        return kwargs



class Login(LoginView):
    def get_success_url(self): #farg in method in ast ke digar be self yani user dastrasi darim.
        user = self.request.user

        if user.is_superuser or user.is_author:
            return reverse_lazy('account:home')
        else:
            return reverse_lazy('account:profile')





class PasswordChange(PasswordChangeView):
    success_url = reverse_lazy('password_change_done')









from django.http import HttpResponse

from .forms import SignupForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token

from django.core.mail import EmailMessage

class Register(CreateView):
    form_class = SignupForm
    template_name = "registration/register.html"

    def form_valid(self,form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()
        current_site = get_current_site(self.request)
        mail_subject = 'فعالسازی اکانت'
        message = render_to_string('registration/activate_account.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
        })
        to_email = form.cleaned_data.get('email')
        email = EmailMessage(
            mail_subject, message, to=[to_email]
        )
        email.send()
        return HttpResponse('<a href = " /login ">ورود</a> لینک فالسازی ارسال شد' )


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()

        return HttpResponse('<a href="/login">اکانت شما با موفقیت فعال شد</a>')
    else:
        return HttpResponse(' <a href="/register">اکانت شما با موفقیت فعال شد</a>این لینک غیر فعال است.')








