from django.contrib import admin
from django.urls import include, path
from skill import views


urlpatterns = [
     path('logout/',views.LogoutPage,name='logout'),
    path('login/', views.login_view, name='login'),
    path('', views.register_view, name='register'),
    path('try/',views.trypage,name='try'),
    path('user_dashboard', views.user_dashboard, name='user_dashboard'),
    path('categorization/', views.categorization, name='categorization'),
    path('jobseeker', views.job_seeker, name='job_seeker'),
    path('all-jobs/', views.all_jobs, name='all_jobs'),
    path('company', views.company, name='company'),
    path('prediction',views.prediction,name='prediction'),
]