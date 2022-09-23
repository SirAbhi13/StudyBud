from . import views
from django.urls import path

app_name = 'base'
urlpatterns = [
    path('login/', views.loginPage, name = 'login'),
    path('register/', views.registerPage, name = 'register'),
    path('logout/', views.logoutPage, name = 'logout'),
    path('',views.home, name= "home"),
    path('room/<str:pk>/',views.room, name='room'),
    path('create-room/',views.createRoom,name='create-room'),
    path('update-room/<str:pk>/',views.updateRoom,name='update-room'),
    path('delete-room/<str:pk>/',views.deleteRoom,name='delete-room'),
    path('delete-message/<str:pk>/',views.deleteMessage,name='delete-message'),

]