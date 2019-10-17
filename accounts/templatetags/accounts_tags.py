from django import template
from ..models import *

register = template.Library()
@register.simple_tag(name = 'total_posts_number') # register the tag

def total_posts(): # returns the total number of posts
    return userPosts.objects.all().count()

@register.inclusion_tag('accounts/home/latest_posts.html')
def show_latest_posts(count = 3):
    latest_posts = userPosts.objects.order_by('-publish').filter(status ='publish')[:count]
    return {'latest_posts':latest_posts}

@register.filter(name='addclass') # custom django forms
def addclass(value, arg):
    return value.as_widget(attrs={'class': arg})
