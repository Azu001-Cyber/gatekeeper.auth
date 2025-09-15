from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField


# Create your models here.

GENDER = [
    ('male', 'MALE'),
    ('female', 'FEMALE'),
    ('other', 'OTHER')

]

class ProfileData(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
    first_name = models.CharField(verbose_name='First Name', blank=False, null=False, max_length=100)
    last_name = models.CharField(verbose_name='Last Name', blank=False, null=False, max_length=100)
    age = models.PositiveIntegerField(verbose_name='Age', blank=True, null=True)
    gender = models.CharField(verbose_name='User Gender', max_length=6, blank=True, default='male', choices=GENDER)
    bio = models.TextField(max_length=250, blank=True, null=True)
    phone = PhoneNumberField()
    image = models.ImageField(null=True, blank=True, upload_to='profile_images/', default='profile_images/default.jpg')
    birth_date = models.DateField(verbose_name='Birth Date', blank=True, null=True)
    location = models.CharField(verbose_name='Location', max_length=100, blank=True)
    date_created = models.DateField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Data Profile'
        verbose_name_plural = "Data Profiles" 


    def display_name(self):
        return f"{self.user.username}'s Profile"
    
    def handle(self):
        return f'@{self.user.username}'
    
    def __str__(self):
        return f'{self.display_name()} ~ {self.handle()}'
    


    



