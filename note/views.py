from django.shortcuts import render, redirect
from django.shortcuts import render
from django.contrib import messages
from datetime import datetime
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from .models import AddNote
from django.db import transaction

# Create your views here.


def index(request):
    if request.user.is_authenticated:
        username = request.user
        notes = AddNote.objects.filter(username=username).all()
        context = {
                    "name" : f"{User.objects.filter(username=username)[0].first_name} {User.objects.filter(username=username)[0].last_name}",
                    "username": username,
                    "notes" : notes
                }
        # Add Note
        if request.method == "POST":
            title = request.POST.get("title")
            desc = request.POST.get("desc")
            addnotes = AddNote(username=username, title=title, desc=desc, date=datetime.today())
            if User.objects.filter(username=username).exists():
                addnotes.save()
        return render(request, "index.html", context)
    else:
        return redirect("login")


def loginPage(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        if User.objects.filter(username=username).exists():
            user =  authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "You Successfully Logged In !")
                return redirect("index")
            else:
                messages.warning(request, "Invalid Username or Password. Please try Again !")
                return render(request, "login.html")
        else:
            return render(request, "login.html")
    return render(request, "login.html")


def registerPage(request):
    if request.method == "POST":
        firstname = request.POST.get("firstname")
        email = request.POST.get("email")
        lastname = request.POST.get("lastname")
        username = request.POST.get("username")
        password = request.POST.get("password")
        if User.objects.filter(username=username).exists():
            messages.warning(request, "Username Already Exists !")
            return render(request, "register.html")
        else:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.first_name = firstname
            user.last_name = lastname
            user.save()
            messages.success(request, "You Successfully Registered !")
            return redirect("login")
    return render(request, "register.html")


def forgotPage(request):
    if request.method == "POST":
        email = request.POST.get("email")
        username = request.POST.get("username")
        newpassword = request.POST.get("newpassword")
        if User.objects.filter(username=username, email=email).exists():
            with transaction.atomic():
                user = User.objects.get(username=username)
                user.set_password(newpassword)
                user.save()
                messages.success(request, "Your Password Saved Successfully !")
                return redirect("/login")
        else:
            messages.warning(request, "Invalid Credentials. Please try Again !")
            return render(request, "forgot.html")
    return render(request, "forgot.html")


def logoutPage(request):
    logout(request)
    return redirect("login")


def update_Password(request):
    if request.method == "POST":
        username = request.user
        prevpassword = request.POST.get("firstPass")
        newpassword = request.POST.get("newpassword")
        user = User.objects.get(username=username)
        if user.check_password(prevpassword) == True:
            with transaction.atomic():
                user.set_password(newpassword)
                user.save()
                messages.success(request, "Your Password Changed Successfully !")
                return redirect('index')
        else:
            messages.warning(request, "Invalid Credentials. Please try Again !")
            return render(request, "updatePassword.html")

    return render(request, "updatePassword.html")


def delnote(request, id):
    if request.method == "GET":
        if request.user.is_authenticated:
            note = AddNote.objects.get(id=id)
            note.delete()
        return redirect("index")
