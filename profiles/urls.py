from django.urls import path , include,re_path , reverse
from django.contrib.auth import views as auth_views
from .views import *

app_name ='profiles'
urlpatterns = [

    path('<slug:username>/post/new/',sharePostView,name = 'share_post'),
    path('<slug:username>/password_change/',
            auth_views.PasswordChangeView.as_view(template_name = "profiles/registration/changePassword.html",
                success_url ='done/'),
                                name='password_change'),
    path('<slug:username>/password_change/done/',
            auth_views.PasswordChangeDoneView.as_view(template_name = "profiles/registration/changePasswordDone.html") ,
                                                name='password_change_done'),
    path('<slug:username>/edit_profile/',edit_profile,name = 'edit_profile'),
    path('<slug:username>/<int:id>/edit_post/',editPost,name = 'edit_post'),
    path('<slug:username>/<int:id>/delete_post/done/',deletePost,name = 'delete_post'),

]
