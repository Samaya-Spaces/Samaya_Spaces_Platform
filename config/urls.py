from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView



# This is the main URL switchboard for your entire project.
urlpatterns = [
    # Core Django and User apps
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/', include('users.urls')),
    path("accounts/", include('allauth.urls')),
    

    # Our Feature Apps
    path('roommates/', include('roommates.urls')),

    # ===================================================================
    path('bookings/', include('bookings.urls')),
    # ===================================================================

  
    path('', include('listings.urls')),
    path('chat/', include('chat.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)