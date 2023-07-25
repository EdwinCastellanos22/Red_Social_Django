from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import CreateView
from apirest.models import Post, Comment, Profile, Chat, Message
from .forms import PostForm, RegisterForm
from django.urls import reverse_lazy
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages

# Create your views here.
class HomeView(CreateView):
    model= Post
    form_class= PostForm
    template_name= "apirest/home.html"
    success_url= reverse_lazy('/')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["posts"] = Post.objects.all()
        context["comments"] = Comment.objects.all()
        context['profile']= Profile.objects.get(user = self.request.user)
        context['postForm']= PostForm()
        return context


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