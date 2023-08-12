from http.client import responses
from django.shortcuts import redirect, render
from django.http import HttpResponse
from .utils import *
from .models import *
from django.utils import timezone
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from .forms import UserRegistrationForm,CSVUploadForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import csv
from django.contrib.auth.hashers import make_password

# Create your views here.

def register(request):
    """
    This function is for new user register.
    """
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login') 
    else:
        form = UserRegistrationForm()
    return render(request, 'artist_data/register.html', {'form': form})



def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        print(user,"------------------------")
        if user is not None:
            login(request, user)
            return redirect('home') 
        else:
            messages.error(request, 'Invalid credentials')
    return render(request, 'artist_data/login.html')


def logout_view(request):
    """
    This function is for  user logout.
    """
    logout(request)
    return redirect('login')

@login_required
def home(request):
    """
    This function is for dashboard.
    """
    return render(request, 'artist_data/dashboard.html')




# For Users
@login_required
def create_user(request):
    """
    This function is for new user register.
    """
    if request.method == 'POST':
        data = request.POST
        current_time = timezone.now()
        query = "INSERT INTO artist_data_user (username,first_name, last_name, email, password, phone, dob, gender, address,is_superuser,is_staff,is_active,date_joined, created_at, update_at) VALUES (%s,%s,%s,%s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        params = (data['username'],data['first_name'], data['last_name'], data['email'], data['password'], data['phone'], data['dob'], data['gender'], data['address'],False,False,False,False, current_time, current_time)
        execute_query(query, params)
        return redirect('all_users')
    return render(request, 'artist_data/user/create_user.html')


# def all_users(request):
#     """
#     This function is for retrieve all user details.
#     """
#     user_query = "SELECT * FROM artist_data_user"
#     users_data = execute_query(user_query)
#     return render(request, 'artist_data/user/all_users.html', {'users_data':users_data})
@login_required
def all_users(request):
    """
    This function is for retrieving all user details and displaying them.
    """
    user_query = "SELECT id,username,first_name, last_name, email, password, phone, dob, gender, address, created_at, update_at FROM artist_data_user"
    users_data = execute_query(user_query)

    formatted_users_data = []
    for user_tuple in users_data:
        user_dict = {
            'id':user_tuple[0],
            'username':user_tuple[1],
            'first_name': user_tuple[2],
            'last_name': user_tuple[3],
            'email': user_tuple[4],
            'password': user_tuple[5],
            'phone': user_tuple[6],
            'dob': user_tuple[7],
            'gender': user_tuple[8],
            'address': user_tuple[9],
            'created_at': user_tuple[10],
            'update_at': user_tuple[11]
        }
        formatted_users_data.append(user_dict)

    return render(request, 'artist_data/user/all_users.html', {'users_data': formatted_users_data})

@login_required
def update_user(request, user_id):
    """
    This function is for update user details.
    """
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        data = request.POST
        query = "UPDATE artist_data_user SET  username=%s,first_name = %s, last_name = %s, email = %s, password = %s, phone = %s, dob = %s, gender = %s, address = %s WHERE id = %s"
        params = (data['username'],data['first_name'], data['last_name'], data['email'], data['password'], data['phone'], data['dob'], data['gender'], data['address'], user_id)
        execute_query(query, params)
        return redirect('all_users')        
    else:
        return render(request, 'artist_data/user/update_user.html', {'user': user})

@login_required
def delete_user(request, user_id):
    if request.method == 'POST':
        query = "DELETE FROM artist_data_user WHERE id = %s"
        params = (user_id,)
        execute_query(query, params)
        messages.success(request, 'User deleted successfully')
        return redirect('all_users')
    else:
        return redirect('all_users')



# For Artist
@login_required
def create_artist(request):
    """
    This function is for create new artist.
    """
    if request.method == 'POST':
        data = request.POST
        current_time = timezone.now()
        query = "INSERT INTO artist_data_artist (name, dob, gender, address, first_release_year, no_of_albums_released, created_at, updated_at) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        params = (data['name'], data['dob'], data['gender'], data['address'], data['first_release_year'], data['no_of_albums_released'], current_time, current_time)
        execute_query(query, params)
        return HttpResponse("Artist created successfully!")
    return render(request, 'artist_data/artist/create_artist.html')

@login_required
def all_artists(request):
    """
    This function is for retrieve all artist.
    """
    query = "SELECT * FROM artist_data_artist"
    artist_data = execute_query(query)
    return render(request, 'artist_data/artist/read_artist.html', {'artist_data':artist_data})


@login_required
def update_artist(request, artist_id):
    """
    This function is for artist update.
    """
    artist = get_object_or_404(Artist, id=artist_id)
    if request.method == 'POST':
        data = request.POST
        query = "UPDATE artist_data_artist SET name = %s, dob = %s, gender = %s, address = %s, first_release_year = %s, no_of_albums_released = %s WHERE id = %s"
        params = (data['name'], data['dob'], data['gender'], data['address'], data['first_release_year'], data['no_of_albums_released'], artist_id)
        execute_query(query, params)
        return HttpResponse('Artist updated successfully!')
    return render(request, 'artist_data/artist/update_artist.html', {'artist': artist})


@login_required
def delete_asrtist(request, artist_id):
    """
    This function is for artist delete.
    """
    if request.method == 'POST':
        query = "DELETE FROM artist_data_artist WHERE id = %s"
        params = (artist_id,)
        execute_query(query, params)
        return HttpResponse('Artist deleted successfully!')
    return redirect('all_artists')

@login_required
def artist_songs(request, artist_id):
    query = """
    SELECT m.id, a.name, m.title, m.album_name, m.genre, m.created_at, m.updated_at
    FROM artist_data_music AS m
    INNER JOIN artist_data_artist AS a ON m.artist_id_id = a.id
    WHERE a.id = %s
    """
    params = (artist_id,)
    rows = execute_query(query,params)
    songs = []
    for row in rows:
        print(row)
        song = {
            'id': row[0],
            'artist': row[1],
            'title': row[2],
            'album_name': row[3],
            'genre': row[4],
            'created_at': row[5],
            'updated_at': row[6],
        }
        songs.append(song)
    
    artist = get_object_or_404(Artist, id=artist_id)
    return render(request, 'artist_data/artist/view_songs.html', {'artist': artist, 'songs': songs})

@login_required
def upload_csv(request):
    """
    This function is for upload artist data as csv formate.
    """
    if request.method == 'POST':
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['csv_file']
            decoded_file = csv_file.read().decode('utf-8')
            csv_data = csv.reader(decoded_file.splitlines(), delimiter=',')
            next(csv_data)  
            for row in csv_data:
                name, dob, gender, address, first_release_year, no_of_albums_released = row
                artist = Artist(name=name, dob=dob, gender=gender, address=address,
                                first_release_year=first_release_year, no_of_albums_released=no_of_albums_released)
                artist.save()
            return redirect('all_artist')  
    else:
        form = CSVUploadForm()
    return render(request, 'artist_data/artist/upload.html', {'form': form})

@login_required
def export_artists_csv(request):
    """
    This function is for export artist data from database.
    """
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="artists.csv"'
    writer = csv.writer(response)
    writer.writerow(['Name', 'Date of Birth', 'Gender', 'Address', 'First Release Year', 'No. of Albums Released'])
    artists = Artist.objects.all()
    for artist in artists:
        writer.writerow([artist.name, artist.dob, artist.get_gender_display(),
                         artist.address, artist.first_release_year, artist.no_of_albums_released])

    return response





# For Musics
@login_required
def create_music(request):
    """
    This function is for create music.
    """
    # artists=Artist.objects.all()
    qr = "SELECT * FROM artist_data_artist" 
    artists=execute_query(qr)
    if request.method == 'POST':
        data = request.POST
        artist_id = data['artist_id']
        artist = get_object_or_404(Artist, id=artist_id)
        current_time = timezone.now()
        query = "INSERT INTO artist_data_music (artist_id_id, title, album_name, genre, created_at, updated_at) VALUES (%s, %s, %s, %s, %s, %s)"
        params = (artist_id, data['title'], data['album_name'], data['genre'], current_time, current_time)
        execute_query(query, params)
        return HttpResponse('Music created successfully!')
    return render(request, 'artist_data/music/create_music.html',{'artists':artists})

@login_required
def all_music(request):
    """
    This function is for all music.
    """
    query = "SELECT * FROM artist_data_music"
    musics = execute_query(query)
    return render(request, 'artist_data/music/read_music.html', {'musics':musics})


@login_required
def update_music(request, music_id):
    """
    This function is for update music.
    """
    music = get_object_or_404(Music, id=music_id)
    if request.method == 'POST':
        data = request.POST
        query = "UPDATE artist_data_music SET artist_id_id = %s, title = %s, album_name = %s, genre = %s WHERE id = %s"
        params = (data['artist_id'], data['title'], data['album_name'], data['genre'], music_id)
        execute_query(query, params)
        return HttpResponse('Music Updated Successfully!')
    else:
        return render(request, 'artist_data/music/update_music.html',{'music':music})
    

@login_required   
def delete_music(request, music_id):
    """
    This function is for delete music.
    """
    if request.method == 'POST':
        query = "DELETE FROM Artist_data_music WHERE id=%s"
        params = (music_id,)
        execute_query(query,params)
        return HttpResponse('Music Deleted Successfully!')
    return render(request, 'artist_data/music/delete_music.html')