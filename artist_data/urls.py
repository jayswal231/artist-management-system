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
    all_users,
    create_user,
    read_user, 
    update_user,
    delete_user,

    create_artist,
    all_artists,
    update_artist,
    delete_asrtist,

    export_artists_csv,
    upload_csv,
)

urlpatterns = [
    path('register/', views.register, name='register'),
    path('', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('home/', views.home, name='home'),
    
    path('user/all/', all_users, name='all_users'),
    path('user/create/', create_user, name='create_user'),
    path('user/read/<int:user_id>/', read_user, name='read_user'),
    path('user/update/<int:user_id>/', update_user, name='update_user'),
    path('user/delete/<int:user_id>/', delete_user, name='delete_user'),

    path('artist/create/', create_artist, name='create_artist'),
    path('artist/all/', all_artists, name='all_artists'),
    path('artist/update/<int:artist_id>/', update_artist, name='update_artist'),
    path('artist/delete/<int:artist_id>/', delete_asrtist, name='delete_artist'),

    path('export-artists-csv/', export_artists_csv, name='export_artists_csv'),
    path('upload/', upload_csv, name='upload_csv'),
]

