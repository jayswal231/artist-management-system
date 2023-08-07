from django.urls import path
from . import views 

# urlpatterns = [
#     path('register/', views.register, name='register'),
#     path('login/', views.login_view, name='login'),
#     path('logout/', views.logout_view, name='logout'),
#     path('home/', views.home, name='home'),

    
# ]

# crud_project/urls.py
from django.urls import path
from artist_data.views import (
    create_user,
    read_user, 
    update_user,
    delete_user,
)

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('home/', views.home, name='home'),
    
    path('user/create/', create_user, name='create_user'),
    path('user/read/<int:user_id>/', read_user, name='read_user'),
    path('user/update/<int:user_id>/', update_user, name='update_user'),
    path('user/delete/<int:user_id>/', delete_user, name='delete_user'),

]

