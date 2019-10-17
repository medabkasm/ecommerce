from django.contrib import admin
from django.urls import path , include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.conf.urls.i18n import i18n_patterns

urlpatterns = i18n_patterns(
    path('admin/', admin.site.urls),
    path('',include('accounts.urls',namespace = 'home' )),
    path('profile/',include('profiles.urls', namespace = 'profiles')),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(
                    template_name ='accounts/registration/password_reset_confirm.html'),
                name='password_reset_confirm'),
    path('reset/done/',auth_views.PasswordResetCompleteView.as_view(
               template_name ='accounts/registration/password_reset_complete.html'),
                   name='password_reset_complete'),
    path('password_reset/',auth_views.PasswordResetView.as_view(
                                template_name ='accounts/registration/password_reset.html',),
                                            name='password_reset'),

    path('password_reset/done/',auth_views.PasswordResetDoneView.as_view(
                    template_name ='accounts/registration/password_reset_done.html'),
                        name='password_reset_done'),
    path('register/social-auth/',include('social_django.urls',	namespace='social')),
    #path('messages/', include('messages.urls')),

)+static(settings.MEDIA_URL ,document_root = settings.MEDIA_ROOT)
