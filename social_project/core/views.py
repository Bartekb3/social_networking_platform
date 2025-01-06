from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from .forms import RegistrationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Post, Comment, Profile
from .forms import PostForm, CommentForm
from django.shortcuts import render, get_object_or_404
from .models import Profile, Post
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib import messages

def signup_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log the user in after successful registration
            return redirect('home')  # Redirect to the homepage
    else:
        form = RegistrationForm()
    return render(request, 'core/signup.html', {'form': form})
class CustomLoginView(LoginView):
    template_name = 'core/login.html'
class CustomLogoutView(LogoutView):
    next_page = 'login'  # Redirect to login page after logout
    



@login_required
def add_friend_view(request, user_id):
    # Get the target user by ID
    target_user = get_object_or_404(User, id=user_id)

    # Get the current user's profile
    current_user_profile = request.user.profile

    # Prevent adding oneself as a friend
    if request.user == target_user:
        messages.error(request, "You cannot add yourself as a friend.")
        return redirect('profile', user_id=user_id)

    # Prevent adding the same friend multiple times
    if target_user in current_user_profile.friends.all():
        messages.warning(request, f"You are already friends with {target_user.username}.")
        return redirect('profile', user_id=user_id)

    # Add the target user as a friend
    current_user_profile.friends.add(target_user.profile)
    messages.success(request, f"You are now friends with {target_user.username}!")
    return redirect('profile', user_id=user_id)






@login_required
def home_view(request):
    # Handle the search query
    query = request.GET.get('q')  # Get the search term from the URL
    search_results = None
    if query:
        search_results = User.objects.filter(
            Q(username__icontains=query) | Q(email__icontains=query)
        )  # Search by username or email

    # Get the current user's friends' posts
    user_friends = request.user.profile.friends.all()
    posts = Post.objects.filter(author__profile__in=user_friends).order_by('-created_at')
    posts |= Post.objects.filter(author=request.user).order_by('-created_at')  # Include own posts

    return render(request, 'core/home.html', {
        'posts': posts,
        'search_results': search_results,
        'query': query,
    })





@login_required
def create_post_view(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user  # Set the logged-in user as the author
            post.save()
            return redirect('home')
    else:
        form = PostForm()
    return render(request, 'core/create_post.html', {'form': form})





# View a single post and its comments
def post_detail_view(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = post.comments.all()  # Fetch all comments for the post
    comment_form = CommentForm()
    return render(request, 'core/post_detail.html', {
        'post': post,
        'comments': comments,
        'comment_form': comment_form,
    })





# Add a comment to a post
@login_required
def add_comment_view(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('post_detail', post_id=post.id)
    return redirect('post_detail', post_id=post.id)





# Like or unlike a post
@login_required
def like_post_view(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.user in post.likes.all():
        post.likes.remove(request.user)  # Unlike the post
        liked = False
    else:
        post.likes.add(request.user)  # Like the post
        liked = True

    return JsonResponse({'liked': liked, 'like_count': post.likes.count()})





@login_required
def profile_view(request, user_id):
    # Get the user's profile
    profile = get_object_or_404(Profile, user_id=user_id)
    
    # Get all posts authored by the user
    posts = Post.objects.filter(author=profile.user).order_by('-created_at')

    # Check if the profile belongs to the logged-in user
    is_own_profile = profile.user == request.user

    return render(request, 'core/profile.html', {
        'profile': profile,
        'posts': posts,
        'is_own_profile': is_own_profile,  # Pass the check to the template
    })
