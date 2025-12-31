from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import User, Post, Comment
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import redirect

def home(request):
    return redirect('feed')

# Registration
def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('feed')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

# Login
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('feed')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

# Feed
@login_required
def feed(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'feed.html', {'posts': posts})

# Create Post
@login_required
def create_post(request):
    if request.method == 'POST':
        Post.objects.create(user=request.user, content=request.POST['content'])
        return redirect('feed')
    return render(request, 'create_post.html')

# Post Detail
@login_required
def post_detail(request, post_id):
    post = Post.objects.get(id=post_id)
    comments = Comment.objects.filter(post=post)
    return render(request, 'post_detail.html', {'post': post, 'comments': comments})

# Add Comment
@login_required
def add_comment(request, post_id):
    if request.method == 'POST':
        Comment.objects.create(post_id=post_id, user=request.user, content=request.POST['content'])
    return redirect('post_detail', post_id=post_id)

# Like Post
@login_required
def like_post(request, post_id):
    post = Post.objects.get(id=post_id)
    if request.user in post.likes.all():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
    return redirect('feed')

# Follow User
@login_required
def follow_user(request, user_id):
    user_to_follow = User.objects.get(id=user_id)
    if request.user in user_to_follow.followers.all():
        user_to_follow.followers.remove(request.user)
    else:
        user_to_follow.followers.add(request.user)
    return redirect('feed')
