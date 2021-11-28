from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',home,name='home'),
    path('viewassignments/<str:pk>', viewassignments,name='viewassignments'),
    path('createcourse',createcourse ,name='createcourse'),
    path('createassignment', createassignment,name='createassignment'),
    path('submitassignment/<str:pk>', submitassignment,name='submitassignment'),
    path('viewSubmissions/<str:pk>', viewSubmissions,name='viewSubmissions'),    
    path('register/',registerPage,name='register'),
    path('login/',loginPage,name='login'),

    path('logout/',logoutUser,name='logout'),
    

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)