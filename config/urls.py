# config/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from roommates.views import signup_view

urlpatterns = [
    path('admin/', admin.site.urls),

    # Authentication
    path('accounts/', include('django.contrib.auth.urls')),
    path('signup/', signup_view, name='signup'),

    # Static pages
    path('help/', TemplateView.as_view(template_name='help.html'), name='help'),
    path('about/', TemplateView.as_view(template_name='about.html'), name='about'),

    # App-specific
    path('accounts/', include('users.urls')),
    path('roommates/', include('roommates.urls')),
    path('bookings/', include('bookings.urls')),
    path('', include('listings.urls')),  # Homepage
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
