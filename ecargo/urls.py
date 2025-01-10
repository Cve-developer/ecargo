from django.urls import path
from . import views

urlpatterns = [
    path('', views.user_login, name="login"),
    path('dashboard/', views.dashboard, name="dashboard"),
    path('logout/', views.logout_view, name='logout'),
    path('user-login/', views.user_login, name="user-login"),
    path('user-register/', views.user_register, name="user-register"),
    path('all-trucks/', views.all_trucks, name="all-trucks"),
    path('all-members/', views.all_members, name="all-members"),
    path('add-truck/', views.add_truck, name="add-truck"),
    path('add-member/', views.add_member, name="add-member"),
    path('single-truck/<int:id>/', views.single_truck, name="single-truck"),
    path('single-member/<int:id>/', views.single_member, name="single-member"),
    path('update-truck/<int:id>/', views.update_truck, name="update-truck"),
    path('update-member/<int:id>/', views.update_member, name="update-member"),
    path('delete-truck/<int:id>/', views.delete_truck, name="delete-truck"),
    path('delete-member/<int:id>/', views.delete_member, name="delete-member"),
    #path('register/', views.user_register, name="register"),   
    
]