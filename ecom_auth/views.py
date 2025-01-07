from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from .utils import TokenGenerator, generate_token
from django.contrib.auth import authenticate,login as auth_login,logout as auth_logout
from django.contrib.auth.tokens import default_token_generator

# Create your views here.
def signup(request):
    if request.method == 'POST':
        email = request.POST.get('email', '')  
        password = request.POST['pass1']
        confirm_password = request.POST['pass2']

        if password != confirm_password:
            messages.warning(request, "Password do not match")
            return render(request, 'signup.html')

        try:
            user = User.objects.get(username=email)
            messages.info(request, "Email already exists.")
            return render(request, 'signup.html')
        except User.DoesNotExist:
            pass

        user = User.objects.create_user(email, email, password)
        user.is_active = True
        user.save()

        messages.success(request, "Signup successful. Please log in.")
        return redirect('/auth/login')

    return render(request, 'signup.html')




from django.contrib.auth import authenticate, login as auth_login

def login(request):
    if request.method == "POST":
        username = request.POST.get('email')
        userpassword = request.POST.get('pass1')
        myuser = authenticate(username=username, password=userpassword)

        if myuser is not None:
            auth_login(request, myuser)
            messages.success(request, 'Login Successfully')
            return redirect('/')
        else:
            messages.error(request, 'Invalid Password')
            return redirect('/auth/login')
    
    return render(request, 'login.html')

def logout(request):
    auth_logout(request)
    messages.info(request, 'Logout Successfully')
    return redirect('/auth/login')