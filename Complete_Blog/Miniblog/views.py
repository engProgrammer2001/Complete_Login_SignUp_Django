from django.shortcuts import render,redirect
from .forms import signUpForm, loginForm, PostForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import Post
from django.contrib.auth.models import Group

# Home.
def home(request):
    posts = Post.objects.all()
    return render(request, 'Miniblog/home.html', {'posts':posts})

# Home.
def about(request):
    return render(request, 'Miniblog/about.html')

# Contact.
def contact(request):
    return render(request, 'Miniblog/contact.html')

# Dashboard.
def dashboard(request):
    if request.user.is_authenticated:
        posts = Post.objects.all()
        user = request.user
        full_name = user.get_full_name()
        group = user.groups.all()
        return render(request, 'Miniblog/dashboard.html', {'posts':posts,'full_name':full_name, 'groups':group})
    else:
        return redirect('/login/')

# logOut.
def user_logout(request):
    logout(request)
    return redirect('home')

# signup.
def user_signup(request):
    if request.method == 'POST':
        form = signUpForm(request.POST)
        if form.is_valid():
            messages.success(request, "Congratulations! - You are successflly SignUped!")
            user = form.save()
            group = Group.objects.get(name='Author')
            user.groups.add(group)
    else:
        form = signUpForm()
    return render(request, 'Miniblog/signup.html',{'form':form})

# login.
def user_login(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = loginForm(request=request, data=request.POST)
            if form.is_valid():
                uname = form.cleaned_data['username']
                upass = form.cleaned_data['password']
                user = authenticate(username=uname, password=upass)
                if user is not None:
                    login(request, user)
                    messages.success(request, "Wel-Come! Logged in Successfully!")
                    return redirect('/dashboard/')
        else:
            form = loginForm()
        return render(request, 'Miniblog/login.html', {'form':form})
    else:
        return redirect('/dashboard/')


# This is For add new post
def addNewPost(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = PostForm(request.POST)
            if form.is_valid():
                # form.save()
                title = form.cleaned_data['title']
                desc = form.cleaned_data['desc']
                post = Post(title=title, desc=desc)
                post.save()
                form = PostForm()
                
        else:
            form = PostForm()
        return render(request, 'Miniblog/addpost.html', {'form':form})
    else:
        return redirect('/login/')
    
# This is For Update new post
def UpdatePost(request, id):
    if request.user.is_authenticated:
        if request.user.is_authenticated:
            if request.method == 'POST':
                pi = Post.objects.get(pk=id)
                form = PostForm(request.POST, instance=pi)
                if form.is_valid():
                    form.save()
            else:
                pi = Post.objects.get(pk=id)
                form = PostForm(instance=pi)
        return render(request, 'Miniblog/updatepost.html', {'form':form})
    else:
        return redirect('/login/')
    
    
# This is For delete post
def deletePost(request, id):
    if request.user.is_authenticated:
        if request.user.is_authenticated:
            if request.method == 'POST':
                pi = Post.objects.get(pk=id)
                pi.delete()
                return redirect('/dashboard/')
    else:
        return redirect('/login/')
    
    