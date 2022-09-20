from email import message
from django.shortcuts import render,redirect
from django.db.models import Q
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth import authenticate, login,logout
from . models import Room, Topic
from . forms import RoomForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm


def loginPage(request):
    page = 'login'

    if request.user.is_authenticated:
        return redirect("base:home")

    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "User doesn't exist")
        
        user = authenticate(request, username=username,password=password)

        if user is not None:
            login(request, user)
            return redirect('base:home')
        else:
            messages.error(request, "Username or password does not exist")

    context = {'page' : page}
    return render(request,'base/login_register.html', context)

def logoutPage(request):
    logout(request)
    return redirect('base:home')

def registerPage(request):
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('base:home')
        else:
            messages.error(request, 'An error occurred during registration')
    return render(request, 'base/login_register.html', {'form': form})


def home(request):
    # list_of_rooms = Room.objects.order_by('created')
    query = request.GET.get('q') if request.GET.get('q') != None else ''
    list_of_rooms = Room.objects.filter(
        Q(topic__name__icontains=query) | 
        Q(name__icontains=query) |
        Q(host__username__icontains=query)
    )
    topics = Topic.objects.all()
    room_count = list_of_rooms.count()
    context = {
        'list_of_rooms' : list_of_rooms,
        'topics' : topics,
        'room_count' : room_count,
    }
    #print (list_of_rooms)
    return render(request, 'base/home.html/',context)

def room(request,pk):
    room = Room.objects.get(pk=int(pk))
    context = {'room' : room }
    return render(request, 'base/room.html', context)

@login_required(login_url='base:login')
def createRoom(request):
    form = RoomForm()
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            room = form.save()
            messages.success(request, 'Room created successfully!')
            print(dir(room))
            return redirect('base:room', pk=room.id)
    context = {'form' : form}
    return render(request, 'base/room_form.html', context)

@login_required(login_url='base:login')
def updateRoom(request,pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance= room)

    if request.user != room.host:
        return HttpResponse('You are not allowed here!  ')

    if request.method == 'POST':
        form = RoomForm(request.POST,instance=room)  # updating the room, using instance paramerter otherwise 
        if form.is_valid():                          # it will create new room with that info    
            form.save()
            return redirect('base:home')
    context = {'form' : form}
    return render(request,'base/room_form.html',context)

@login_required(login_url='base:login')
def deleteRoom(request,pk):
    room  = Room.objects.get(id=pk)

    if request.user != room.host:
        return HttpResponse('You are not allowed here!  ')

    if request.method == 'POST':
        room.delete()
        return redirect('base:home')

    return render(request, 'base/delete.html',{'obj': room})
