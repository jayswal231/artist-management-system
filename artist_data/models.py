from django.db import models

# Create your models here.
GENDER_CHOICES = (
        ('m', 'Male'),
        ('f', 'Female'),
        ('o', 'Other'),
    )
class User(models.Model):
    """
    This model for users. 
    """
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    emai = models.EmailField(null=True, blank=True)
    password = models.CharField(max_length=500)
    phone = models.CharField(max_length=20)
    dob = models.DateTimeField(null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='m')
    address = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.first_name
    


class Artist(models.Model):
    """
    This model for artist. 
    """
    name = models.CharField(max_length=255)
    dob = models.DateTimeField(null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='m')
    address = models.CharField(max_length=255)
    first_release_year = models.DateField(null=True, blank=True)
    no_of_albums_released = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    


class Music(models.Model):
    """
    This model for music. 
    """
    GENRE_CHOICES = (
        ('rnb', 'Rhythm and Blues'),
        ('country', 'Country'),
        ('classic', 'Classic'),
        ('rock', 'Rock'),
        ('jazz', 'Jazz'),
    )

    artist_id = models.ForeignKey(Artist, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    album_name = models.CharField(max_length=255)
    genre = models.CharField(max_length=10, choices=GENRE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title