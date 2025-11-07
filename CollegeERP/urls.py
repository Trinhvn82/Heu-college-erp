from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
import notifications.urls
from debug_toolbar.toolbar import debug_toolbar_urls
from sms.forms import CustomAuthenticationForm
from sms import views as sms_views

urlpatterns = [
    path('heuadmin/', admin.site.urls),
    path('', include('sms.urls')),
    path('info/', include('info.urls')),
    path('shop/', include('shop.urls')),
    path('sms/', include('sms.urls')),
    path('tracker/', include('tracker.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('htmx/', include('htmx_patterns.urls')),

    path('notifications/', include(notifications.urls, namespace='notifications')),

    path('accounts/login/',
         auth_views.LoginView.as_view(template_name='sms/login.html', authentication_form=CustomAuthenticationForm), name='login'),
     path('accounts/login-modal/', sms_views.login_modal, name='login_modal'),
    path('accounts/logout/',
         auth_views.LogoutView.as_view(template_name='sms/logout.html'), name='logout'),

    #path('password_reset/', auth_views.PasswordResetView.as_view(template_name='password_reset_form.html'), name='password_reset'),
    #path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),
    #path('password_reset_confirm/uidb64/token/',auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'), name='password_reset_confirm'),
    #path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),

    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    ] + debug_toolbar_urls()

from django.conf import settings
from django.conf.urls.static import static


#if settings.DEBUG:
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
