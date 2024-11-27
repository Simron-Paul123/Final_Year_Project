from django.contrib import admin
from django.urls import include, path
from skill import views


urlpatterns = [
     path('logout/',views.LogoutPage,name='logout'),
    path('login/', views.login_view, name='login'),
    path('', views.register_view, name='register'),

    path('user_dashboard', views.user_dashboard, name='user_dashboard'),
    path('jobseeker', views.job_seeker, name='job_seeker'),
    path('company', views.company, name='company'),
]