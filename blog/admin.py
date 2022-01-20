from django.contrib import admin
from .models import Article,Category,IPAddress

def make_published(modeladmin,request,queryset):
    queryset.update(status = 'p')
make_published.short_description = 'انتشار مشاورات انتخاب شده'

def make_drafted(modeladmin,request,queryset):
    queryset.update(status = 'd')
make_drafted.short_description = 'پیش نویس مشاورات انتخاب شده'

def make_actived(modeladmin,request,queryset):
    queryset.update(status = True)
make_actived.short_description = 'فعال کردن دسته بندی انتخاب شده'

def not_active(modeladmin,request,queryset):
    queryset.update(status = False)
not_active.short_description = 'غیر فعال کردن دسته بندی انتخاب شده '

class CategoryAdmin(admin.ModelAdmin):

    list_display = ('title','parent','status')
    list_filter = (['status'])
    actions = [make_actived,not_active]


admin.site.register(Category,CategoryAdmin)



class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title','thumbnail_tag','author','is_special','status','cat_to_str')
    list_filter = ('status','author')
    search_fields = ('title','description')
    prepopulated_fields = {'slug':('title',)}
    ordering = ['status','created']
    actions = [make_published,make_drafted]




admin.site.register(Article,ArticleAdmin)
admin.site.register(IPAddress)
# Register your models here.