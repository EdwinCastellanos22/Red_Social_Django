from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import CreateView
from apirest.models import Post, Comment, Profile, Chat, Message
from .forms import PostForm, RegisterForm
from django.urls import reverse_lazy
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
import pyrebase

#Settings Firebase
config = {
    "apiKey": "AIzaSyA2Ig4L5cSJHIgE1UCWj6y5Iizu5w_aJpQ",
    "authDomain": "django-api-730e4.firebaseapp.com",
    "projectId": "django-api-730e4",
    "storageBucket": "django-api-730e4.appspot.com",
    "messagingSenderId": "611779181554",
    "appId": "1:611779181554:web:d6839ce3da55ac88be496b",
    "measurementId": "G-L0RP3PSEJV",
    "databaseURL": "https://django-api-730e4-default-rtdb.firebaseio.com/"
}
firebase= pyrebase.initialize_app(config)
auth= firebase.auth()
database= firebase.database()
storage= firebase.storage()

# Create your views here.
def HomeView(request):

    if request.method == 'POST':
        form= PostForm(request.POST, request.FILES)
        form.user= request.user
        if form.is_valid():
            form.save()
            messages.success(request, "Success!")
            return redirect('/')
    else:
        form = PostForm()
    return render(request, 'apirest/home.html', {
        "posts": Post.objects.all(),
        'comments': Comment.objects.all(),
    })

# >>>>>>> 18bae8e79b277981680ffd2d1772896169ae1008

def Login(request):
    if request.method == 'POST':
        username= request.POST['username']
        password= request.POST['password']
        user= authenticate(request, username=username, password= password)
        if user is not None:
            login(request, user)
            messages.success(request, f"Bienvenido {username}")
            return redirect('/')
        else:
            return render(request, 'apirest/login.html', {'error':'Credenciales Invalidas!!'})
    return render(request, 'apirest/login.html')

def Logout(request):
    logout(request)
    return redirect('/')

def RegisterUser(request):
    if request.method == 'POST':
        form= RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Usuario creado exitosamente!.")
            return redirect('/')
    else:
        form= RegisterForm()
    # print(form)
    errors= form.errors
    return render(request, 'apirest/register.html', {'form':form, 'errors':errors})

def NewComment(request, pid):
    if request.method == 'POST':
        comment = Comment()
        comment.author = request.user
        post = Post.objects.get(post_id=pid)
        comment.post= post
        comment.content= request.POST['content']
        comment.save()
        return redirect('/')



def Like(request, post_id):
    post= get_object_or_404(Post, post_id= post_id)
    user= request.user

    if user in post.likes.all():
        post.likes.remove(user)
    else:
        if user in post.dislikes.all():
            post.dislikes.remove(user)
        post.likes.add(user)

    return redirect('/')

def Dislike(request, post_id):
    post= get_object_or_404(Post, post_id= post_id)
    user= request.user

    if user in post.dislikes.all():
        post.dislikes.remove(user)
    else:
        if user in post.likes.all():
            post.likes.remove(user)
        post.dislikes.add(user)

    return redirect('/')

def Chats(request):
    messages_chat= Message.objects.filter(sender= request.user)
    chats= Message.objects.all()

    ctx= {
        "msg" : chats
    }

    return render(request, 'apirest/chat.html', ctx)

def newPost(request):
    if request.method == 'POST' and request.FILES['image']:
        post = Post()
        file= request.FILES['image']
        post.image= file
        post.title = request.POST['title']
        post.content= request.POST['content']
        post.user= request.user
        post.save()
        storage.child('images/'+file.name).put(file.name)
        messages.success(request, f"Posted <<{request.POST['title']}>>")
    return redirect('/')

def newImageProfile(request):
    if request.method == 'POST' and request.FILES['image']:
        file= request.FILES['image']
        profile= Profile.objects.get(user=request.user)
        profile.image= file
        profile.save()
        messages.success(request, 'Imagen Cambiada Exitosamente')
    return redirect('/')

def settingProfile(request):
    user = User.objects.get(id=request.user.id)
    if request.method == 'POST':
        user.first_name= request.POST['first_name']
        user.last_name= request.POST['last_name']
        user.username= request.POST['username']
        user.email= request.POST['email']
        user.save()
        messages.success(request, 'Usuario Actualizado!')
    return redirect('/')