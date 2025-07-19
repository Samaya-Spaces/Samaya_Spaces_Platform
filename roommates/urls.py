from django.urls import path
from . import views

urlpatterns = [
    path('', views.RoommateProfileListView.as_view(), name='profile_list'),
    path('my-profile/', views.my_profile_view, name='my_profile'),
    path('new/', views.RoommateProfileCreateView.as_view(), name='profile_create'),
    path('<int:pk>/', views.RoommateProfileDetailView.as_view(), name='profile_detail'),
    path('<int:pk>/edit/', views.RoommateProfileUpdateView.as_view(), name='profile_update'),
]