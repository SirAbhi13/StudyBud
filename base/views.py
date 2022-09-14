from django.shortcuts import render,redirect
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth import authenticate, login
from . models import Room, Topic
from . forms import RoomForm


def loginPage(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get("password")

        try:
            user = User.objects.get(username = username)
        except:
            messages.error(request, 'User Does not exist!!!!')
        
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request,user)
            return redirect('base:home')
        
        else:
            messages.error(request, "username or password is wrong!!")

    context = {}
    return render(request,'base/login_register.html', context)

def logoutPage(request):
    pass

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

def updateRoom(request,pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance= room)

    if request.method == 'POST':
        form = RoomForm(request.POST,instance=room)  # updating the room, using instance paramerter otherwise 
        if form.is_valid():                          # it will create new room with that info    
            form.save()
            return redirect('base:home')
    context = {'form' : form}
    return render(request,'base/room_form.html',context)


def deleteRoom(request,pk):
    room  = Room.objects.get(id=pk)
    if request.method == 'POST':
        room.delete()
        return redirect('base:home')

    return render(request, 'base/delete.html',{'obj': room})
