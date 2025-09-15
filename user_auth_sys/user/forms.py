
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from crispy_forms.helper import FormHelper

from user.models import ProfileData


# Create forms here

class SignUpForm(UserCreationForm):
    username = forms.CharField(strip=True, required=True)
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={"placeholder":'Enter Email'}), help_text='example@gmail.com')

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password1',
            'password2',
        ]

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email__iexact=email).exists():
            raise ValidationError('Email already exists')
        return email
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.form_action = '' #submit to current url
        self.helper.form_method = 'post'
        self.helper.form_id = 'login_form'
        self.helper.label_class = 'form-helper'
        self.helper.form_class = 'form-control'
    
    

class LoginForm(forms.Form):
    email = forms.EmailField(required=True, max_length=150, widget=forms.EmailInput(attrs={'placeholder':'Your Email'}), help_text='example@gmail.com')
    password = forms.CharField(required=True, max_length=50,widget=forms.PasswordInput(attrs={'placeholder':'Your Password'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.form_action = '' #submit to current url
        self.helper.form_method = 'post'
        self.helper.form_id = 'login_form'
        self.helper.label_class = 'form-helper'
        self.helper.form_class = 'form-control'
        


class ProfileForm(forms.ModelForm):
    birth_date = forms.DateField(widget=forms.DateInput(attrs={'type':'date'}))
    class Meta:
        model = ProfileData
        fields = [
                'first_name',
                'last_name',
                'age',
                'gender',
                'bio',
                'phone',
                'image',
                'birth_date',
                'location'
                ]
        
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

            self.helper = FormHelper(self)
            self.helper.form_action = '' #submit to current url
            self.helper.form_method = 'post'
            self.helper.form_id = 'login_form'
            self.helper.form_class = 'form-control'
            self.helper.label_class = 'form-helper'