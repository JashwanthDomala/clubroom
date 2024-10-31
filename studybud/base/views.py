from django.shortcuts import render,redirect
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout
from django.db.models import Q
from .models import Room,Topic
from .form import RoomForm

# Create your views here.

def home(request):
   # q = request.GET.get('q')
   # rooms = Room.objects.filter(topics__name = q)
    q =request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(
        Q(topic__name__icontains= q) | Q(name__icontains = q) | Q(discription__icontains=q) | Q(host__username__icontains= q)
        )
    topics = Topic.objects.all()
    room_count = rooms.count()
    context = {'rooms':rooms , 'topics':topics , 'room_count': room_count}
    return render(request,'base/home.html',context)

def room(request,pk):
    room = Room.objects.get(id=pk)
    context = {'room': room}
    return render(request,'base/room.html',context)



@login_required(login_url='login')
def createRoom(request):
    
    form = RoomForm()
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form': form}
    return render(request,'base/room_form.html',context)


@login_required(login_url='login')
def updateRoom(request,pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    if request.user == room.host:
        if request.method == 'POST':
            form = RoomForm(request.POST , instance = room )
            if form.is_valid():
                form.save()
                return redirect('home')
        context={'form': form}
        return render(request,'base/room_form.html', context)
    else:
        return HttpResponse('You are not allowed')



@login_required(login_url='login')
def deleteRoom(request,pk):
    room = Room.objects.get(id=pk) 
    if request.user == room.host:
        
        if request.method == 'POST':
            room.delete()
            return redirect('home')
        return render(request,'base/delete.html',{'obj':room})
    else:
        return HttpResponse('You are not allowed')



def loginPage(request):
    if request.user.is_authenticated:
        return render('home')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request,'User not found')
        
        user = authenticate(request,username=username,password=password)

        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,'wrong Password Or username')
    context={}        
    return render(request,'base/login_register.html',context)




def logoutUser(request):
    logout(request)
    return redirect('home')


