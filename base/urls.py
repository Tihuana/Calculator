from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('team/<int:id>/', views.team, name='team'),

    path('create-team/', views.create_team, name='create-team'),
    path('edit-team/<int:id>/', views.edit_team, name='edit-team'),
    path('delete-team/<int:id>/', views.delete_team, name='delete-team'),
    
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
]
