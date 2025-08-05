# renting_service/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings  
from django.conf.urls.static import static  #<-- ADD THIS IMPORT

# We no longer need the render import here

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/', include('users.urls')),
    path("accounts/", include('allauth.urls')),
    path('roommates/', include('roommates.urls')),
    path('', include('listings.urls')), ]

# This is NOT for production! Only for development (DEBUG=True)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


    path('bookings/', include('bookings.urls')),

    # This path is for listings and MUST be last, as it's the catch-all
    path('', include('listings.urls')),
