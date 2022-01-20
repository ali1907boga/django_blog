from django.db import models
from django.utils import timezone

from account.models import User
from django.urls import reverse

#my managers
from django.utils.html import format_html
from django.contrib.contenttypes.fields import GenericRelation
from comment.models import Comment
from star_ratings.models import UserRating,Rating


class ArticleManager(models.Manager):
    def published(self):
        return self.filter(status='p')

class CategoryMnager(models.Manager):
    def active(self):
        return self.filter(status=True)

class IPAddress(models.Model):
    ip_address = models.GenericIPAddressField(verbose_name='آدرس ip')







class Category(models.Model):

    parent = models.ForeignKey('self',default=None,blank=True,null=True,on_delete=models.SET_NULL,related_name='children',verbose_name='زیر دسته')
    title = models.CharField(max_length=100,verbose_name='عنوان')
    slug = models.CharField(max_length=100,unique=True,verbose_name='آدرس')
    status = models.BooleanField(default=False,verbose_name='وضعیت')

    class Meta:
        verbose_name = 'دسته'
        verbose_name_plural = 'دسته ها'

    def __str__(self):
        return self.title

    objects = CategoryMnager()
class Article(models.Model):

    STATUS_CHOICES = (
        ('d','پیش نویس'),
        ('p','منتشر شده')
    )

    title = models.CharField(max_length=100,verbose_name='عنوان')
    slug = models.CharField(max_length=100,unique=True,verbose_name='آدرس')
    category = models.ManyToManyField(Category,related_name='articles')
    description = models.TextField(verbose_name='محتوا')
    thumbnail = models.ImageField(upload_to="images",verbose_name='تصویر')
    author = models.ForeignKey(User,on_delete=models.CASCADE,verbose_name='نویسنده',related_name='articles')
    created = models.DateTimeField(auto_now_add=True,verbose_name='تاریخ انتشار')
    publish = models.DateTimeField(default=timezone.now,verbose_name='زمان انتشار')
    is_special = models.BooleanField(default=False,verbose_name='مقاله ویزه')
    status = models.CharField(max_length=1,choices=STATUS_CHOICES,verbose_name='وضعیت')
    comments = GenericRelation(Comment)
    hits = models.ManyToManyField(IPAddress,through= 'ArticleHit' ,blank=True,related_name='hits',verbose_name='بازدید ها')
    ratings = GenericRelation(Rating)

    class Meta:
        verbose_name = 'مقاله'
        verbose_name_plural = 'مقالات'

    def __str__(self):
        return self.title

    def category_published(self):
        return self.category.filter(status=True)

    def get_absolute_url(self):
        return reverse('account:home')
    def thumbnail_tag(self):
        return format_html("<img width=100 height:75 style='border-radius:5px;' src='{}'>".format(self.thumbnail.url))
    thumbnail_tag.short_description = 'تصویر'

    def cat_to_str(self):
        return ", ".join([category.title for category in self.category_published()])

    cat_to_str.short_description = "دسته بندی"


    objects = ArticleManager()
# Create your models here.

class ArticleHit(models.Model):
    article = models.ForeignKey(Article,on_delete=models.CASCADE)
    ip_address = models.ForeignKey(IPAddress,on_delete=models.CharField)
    created = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ انتشار')


#my managers
