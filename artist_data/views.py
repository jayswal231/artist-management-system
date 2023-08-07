from django.shortcuts import redirect, render
from django.http import HttpResponse
from .utils import *
from .models import *
from django.utils import timezone
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from .forms import UserRegistrationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
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
    """
    This function is for registered user login.
    """
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  
        else:
            messages.error(request, 'Invalid login credentials.')
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
    return render(request, 'artist_data/home.html')


def create_user(request):
    """
    This function is for new user register.
    """
    if request.method == 'POST':
        data = request.POST
        current_time = timezone.now()
        query = "INSERT INTO artist_data_user (username,first_name, last_name, email, password, phone, dob, gender, address, created_at, update_at) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        params = (data['username'],data['first_name'], data['last_name'], data['email'], data['password'], data['phone'], data['dob'], data['gender'], data['address'], current_time, current_time)
        execute_query(query, params)
        return JsonResponse({'message': 'User created successfully'})
    return render(request, 'artist_data/user/create_user.html')



def read_user(request, user_id):
    """
    This function is for view specific user details.
    """
    user_query = "SELECT * FROM artist_data_user WHERE id = %s"
    params = (user_id,)
    user_data = execute_query(user_query, params)

    if user_data:
        user = user_data[0] 
        user_dict = {
            'id': user[0],
            'username': user[1],
            'first_name': user[2],
            'last_name': user[3],
            'email': user[4],
            'phone': user[6],
            'dob': user[7],
            'gender': user[8],
            'address': user[9],
            'created_at': user[10],
            'updated_at': user[11],
        }
        return render(request, 'artist_data/user/read_user.html', {'user': user_dict})
    else:
        return JsonResponse({'message': 'User not found'}, status=404)



def update_user(request, user_id):
    """
    This function is for update user details.
    """
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        data = request.POST
        query = "UPDATE artist_data_user SET username = %s, first_name = %s, last_name = %s, email = %s, password = %s, phone = %s, dob = %s, gender = %s, address = %s WHERE id = %s"
        params = (data['username'],data['first_name'], data['last_name'], data['email'], data['password'], data['phone'], data['dob'], data['gender'], data['address'], user_id)
        execute_query(query, params)
        return JsonResponse({'message': 'User updated successfully'})
        
    else:
        return render(request, 'artist_data/user/update_user.html', {'user': user})




def delete_user(request, user_id):
    """
    This function is for delete user .
    """
    if request.method == 'POST':
        query = "DELETE FROM artist_data_user WHERE id = %s"
        params = (user_id,)
        execute_query(query, params)
        return JsonResponse({'message': 'User deleted successfully'}, status=204)
    else:
        return redirect('read_user')




