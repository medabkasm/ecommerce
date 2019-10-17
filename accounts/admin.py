from django.contrib.auth import get_user_model
from django.contrib import admin
from .models import *


User = customUser

class postsAdmin(admin.ModelAdmin):
    #prepopulated_fields	= {'slug': ('title',)}
    date_hierarchy = 'publish'

admin.site.register(User)
admin.site.register(Image)
admin.site.register(message)
admin.site.register(Profile)
admin.site.register(userPosts,postsAdmin)
