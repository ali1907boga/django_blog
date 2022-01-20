from django import template
from django.db.models import Count,Q,Max
from datetime import datetime,timedelta
from ..models import Category,Article


register = template.Library()

@register.simple_tag
def title():
    return "مشاور من"


@register.inclusion_tag("partials/category_navbar.html")
def category_navbar():
    return {
        'category':Category.objects.filter(status=True)
    }


@register.inclusion_tag('partials/sidebar.html')

def hot_articles():
    last_mounth = datetime.today() - timedelta(days=30)

    return {
        'articles':Article.objects.published().annotate(count = Count('comments',filter=Q(comments__posted__gt = last_mounth) and Q(comments__content_type_id = 6))).order_by('-count','created'),
        'title':'مقالات داغ ماه'
    }

@register.inclusion_tag('partials/sidebar.html')

def hot_articles():
    last_mounth = datetime.today() - timedelta(days=30)

    return {
        'articles':Article.objects.published().annotate(count = Count('hits',filter=Q(articlehit__created__gt = last_mounth))).order_by('-count','created'),
        'title':'مقالات داغ ماه'
    }



