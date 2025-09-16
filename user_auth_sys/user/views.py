from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from user.forms import ProfileForm, SignUpForm, LoginForm
from user.models import ProfileData
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate, get_user_model
from django.views.decorators.http import require_GET
#EMAIL VERIFICATION
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import send_mail
from django.conf import settings
# testing email backend

# handel email error
import logging
logger = logging.getLogger(__name__) #logging email error

# instancilize a global variable to access the user model
user_model = get_user_model()

# Create your views here.



def home(request):
    return render(request, 'user/index.html')


# SignUp
@require_http_methods(["GET", "POST"])
def Signup(request):
    if request.method=="GET":
        form = SignUpForm()
        return render(request, "user/signup.html", {'signup_form':form})
        
    
    if request.method=="POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False 
            user.save()

            # generate activation link
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            activation_path = f'/user/activate/account/{uid}/{token}/'
            activation_link = request.build_absolute_uri(activation_path)
            
            try:
                send_mail(
                subject='Activate your account',
                message=f'Click the link to verify your account: {activation_link}',
                from_email= settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=False
                )
                messages.info(request, "Account Created! Check your email to activate.")
                return redirect('verify_email')
            except Exception as e:
                logger.error(f'Error sending email failed for {user.email}: {e}')
                messages.error(request, 'Something went wrong while sending the email.')
        else:
            form = SignUpForm()
            messages.error( request, "Invalid Informations Provided.")
        return render(request, "user/signup.html", {'signup_form':form})

# --- 

# Activate account

def ActivateView(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = user_model.objects.get(pk=uid)
    except (Exception, user_model.DoesNotExist):
        user = None
    
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "Your account is now active. You can log in.")
        return redirect('login')
    else:
        messages.error(request, "Activation link is invalid.")
        return redirect('signup')


# login
def LoginView(request):
    if request.method=="GET":
        form = LoginForm()
        return render(request, 'user/login.html', {'login_form':form})
    
    if request.method=="POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            try:
                user_obj = user_model.objects.get(email=email)
                username = user_obj.username
                user = authenticate(request, username=username, password=password)
            except user_model.DoesNotExist:
                user = None
            
            if user is not None:
                login(request, user)
                if ProfileData.objects.filter(user=user).exists():
                    return redirect('profile')
                else:
                    return redirect('create_profile')
            else:
                form = LoginForm()
                messages.warning(request, "Invalid Email or Password.")
            return render(request, 'user/login.html', {"login_form":form})
        

@require_GET
def verify_view(request):
    return render(request, 'user/email_verify.html')

def LogoutView(request):
    logout(request)
    return redirect("home")


@login_required(login_url="login")
def ProfileView(request):
    try:
        profile = ProfileData.objects.get(user=request.user)
        has_profile  = True
    except ProfileData.DoesNotExist:
        profile = None
        has_profile = False
    return render(request, 'user/profile.html', {'profile_info': profile, 'has_profile': has_profile})


# CRUD Operations
@require_http_methods(["GET", "POST"])
@login_required(login_url='login')
def create_profile(request):
    # check if profile alredy exists
    if request.method=='GET':
        form = ProfileForm()
        return render(request, 'user/create_profile.html', {'form':form})
    
    if hasattr(request.user, 'profile'):
        messages.warning(request, 'Profile Already Exits.')
        return redirect('profile')

    if request.method=="POST":
        form = ProfileForm(request.POST, request.FILES) # request.FILES for images
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user #attach profile to log in user
            profile.save()
            messages.success(request, 'Your profile has been created')
            return redirect('profile')
    return render(request, 'user/create_profile.html', {'form':form})


@login_required(login_url='login')
def search_user(request):
    query = request.GET.get("query")
    search_result = []
    if query:
        search_result = ProfileData.objects.filter(user__username__icontains=query)
        if not search_result:
            messages.info(request, 'No profile found matching your search.')
    else:
        messages.warning(request, "Please enter a username to search.")
    return render(request, 'user/search.html', {'search_result':search_result, 'query':query})


@login_required(login_url='login')
def retrive_user_profile(request, username):
    try:
        user_profile = ProfileData.objects.get(user__username=username)
        has_profile =True
    except ProfileData.DoesNotExist:
        user_profile = None
        has_profile = False
    return render(request, 'user/user_profile.html', {'user_info': user_profile, 'has_profile':has_profile})
    ...

        
    
@login_required(login_url='login')
def edit_profile(request):
    data = get_object_or_404(ProfileData, user=request.user)

    if request.method=='POST':
        form = ProfileForm(request.POST, request.FILES, instance=data)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileForm(instance=data)
    return render(request, 'user/edit_profile.html', {'edit_form': form})

@login_required(login_url='login')
def delete_profile(request):
    user_profile = get_object_or_404(ProfileData, user=request.user)
    user_profile.delete()
    return redirect('home')



# handles user account deletion
@login_required(login_url='login')
def delete_account(request):
    user_account = request.user
    user_account.delete()
    messages.success(request, "Your account has successfully been deleted.")
    return redirect('home')


