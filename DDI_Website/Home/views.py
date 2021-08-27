from django.shortcuts import render
from django_celery_results.models import TaskResult
from django.contrib.auth import authenticate,login,logout
from django.shortcuts import redirect,HttpResponseRedirect
from Website_Settings import settings
from django.contrib.messages import error
from django.contrib.auth.models import User,Permission
from .models import UserExtensionModel
from django.contrib.auth.hashers import make_password
from .forms import Register,Login


# Create your views here.

def home_page(request):
    homeHTML = 'Home/index.html'
    return render(request,homeHTML)

def login_page(request):
    """
    Get username and password from the form, and if its legal, then let you login
    """
    loginHTML = 'Home/login.html'

    LoginForm = Login()

    if request.method == 'POST':
        LoginForm = Login(request.POST)
        if LoginForm.is_valid():
            username = LoginForm.cleaned_data['username']
            password = LoginForm.cleaned_data['password']
            User = authenticate(username = username,password = password)
            if User is not None: # IF User is in database, then log in, else redirect to login//do nothing
                login(request,User)
                return redirect('%s?next=%s' % (settings.LOGIN_REDIRECT_URL, request.path))
            else:
                error(request,"User or Password not correct")
                return redirect('/login/')
        else:
            error(request,"User or Password not correct")
            return redirect('/login/')
            
                
    context = {
        'Loginform': LoginForm,
    }
    return  render(request,loginHTML,context)

def logout_page(request):
    logout(request)
    logoutHTML = 'Home/logout.html'
    return render(request,logoutHTML)

def registration_page(request):
    """
    Create Username and Password from the form, and if its legal
    It'll log you in, and register you 
    """
    registrationForm = Register()

    registerHTML = 'Home/register.html'

    if request.method == 'POST':
        registrationForm = Register(request.POST)
        if registrationForm.is_valid():
            username = registrationForm.cleaned_data['username']
            password = registrationForm.cleaned_data['password']
            first_name = registrationForm.cleaned_data['first_name']
            last_name = registrationForm.cleaned_data['last_name']
            # Get all information from the fields
            permission = Permission.objects.get(name='Can view task result')
            u = User.objects.filter(username = username).exists() # checks to see if username is in database
            if u: # IF User is in database, then log in, else redirect to register//make new User object
                error(request,"User is already in database")
                return redirect('/register/')
            else:
                User.objects.create(
                    username = username,
                    password = make_password(password),
                    is_superuser = False,
                    first_name = first_name,
                    last_name = last_name,
                    is_staff = True,
                ).save()
                user = authenticate(username = username, password = password)
                userModel = User.objects.get(username = username)
                userModel.user_permissions.add(permission)
                userModel.save()
                # Init the user extension model for new users
                UserExtensionModel(
                    user = userModel,
                    arrayTasksCompleted = [],
                ).save()
                login(request,userModel)
                return redirect('/')
            
    context = {
        'registerForm': registrationForm,
    }        
    return render(request,registerHTML,context)


