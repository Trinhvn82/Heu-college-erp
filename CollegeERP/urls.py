from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
import notifications.urls
from debug_toolbar.toolbar import debug_toolbar_urls

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
         auth_views.LoginView.as_view(template_name='sms/login.html'), name='login'),
    path('accounts/logout/',
         auth_views.LogoutView.as_view(template_name='sms/logout.html'), name='logout'),
] + debug_toolbar_urls()

from django.conf import settings
from django.conf.urls.static import static


#if settings.DEBUG:
#urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
