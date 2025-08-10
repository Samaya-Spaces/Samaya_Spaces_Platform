
from django.urls import path
from . import views

# This line is CRITICAL. It creates the 'roommates' namespace.
# Without this, {% url 'roommates:list' %} will fail.
app_name = 'roommates'

# This is the "phonebook" for the roommates app.
urlpatterns = [
    # This line connects the empty path ('') for this app 
    # (which will be at /roommates/) to the ProfileListView 
    # and gives it the name 'list'.
    # This is the definition for 'roommates:list'.
    path('', views.RoommateProfileListView.as_view(), name='list'),

    # The rest of the URLs for this app
    path('my-profile/', views.my_profile_view, name='my_profile'),
    path('new/', views.RoommateProfileCreateView.as_view(), name='profile_create'),
    path('<int:pk>/', views.RoommateProfileDetailView.as_view(), name='profile_detail'),
    path('<int:pk>/edit/', views.RoommateProfileUpdateView.as_view(), name='profile_update'),
]
