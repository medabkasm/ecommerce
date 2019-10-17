from django.urls import path , include,re_path
from django.contrib.auth import views as auth_views
from django.contrib.auth import views as auth_views

from .views import *

app_name ='accounts'

urlpatterns = [
    #path('',userAccountView.as_view(), name = 'users_presentation'), # (users home)
    path('account/follow/',userFollow,	name='user_follow'),
    path('account/<slug>/',userAccountDetailView,name = 'user_account'),
    path('',usersPostsView,name ='users_posts'), #  users posts (home page)
    path('post/<username>/<id>/',postDetailsView,name = 'post'), #post details
    path('login/',auth_views.LoginView.as_view(template_name = 'accounts/registration/login.html' , redirect_authenticated_user = True),
        name = 'login'),
    path('logout/',auth_views.LogoutView.as_view(template_name = 'accounts/registration/logged_out.html'),
        name = 'logout'),
    path('register/',register,name = 'register'),

]
