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
from .forms import ProfilePictureForm

def signup_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  
            return redirect('home')  
    else:
        form = RegistrationForm()
    return render(request, 'core/signup.html', {'form': form})
    



@login_required
def add_friend_view(request, user_id):

    target_user = get_object_or_404(User, id=user_id)

    current_user_profile = request.user.profile

    if request.user == target_user:
        messages.error(request, "You cannot add yourself as a friend.")
        return redirect('profile', user_id=user_id)

    if target_user in current_user_profile.friends.all():
        messages.warning(request, f"You are already friends with {target_user.username}.")
        return redirect('profile', user_id=user_id)

    current_user_profile.friends.add(target_user.profile)
    messages.success(request, f"You are now friends with {target_user.username}!")
    return redirect('profile', user_id=user_id)


@login_required
def send_friend_request_view(request, user_id):
    target_user = get_object_or_404(User, id=user_id)
    target_profile = target_user.profile
    current_profile = request.user.profile

    if target_profile in current_profile.friends.all():
        messages.warning(request, f"{target_user.username} is already your friend.")
    elif current_profile in target_profile.friend_requests.all():
        messages.warning(request, f"You have already sent a friend request to {target_user.username}.")
    else:
        target_profile.friend_requests.add(current_profile)
        messages.success(request, f"Friend request sent to {target_user.username}.")

    return redirect('profile', user_id=target_user.id)

@login_required
def accept_friend_request_view(request, user_id):
    sender = get_object_or_404(User, id=user_id)
    sender_profile = sender.profile
    current_profile = request.user.profile

    if sender_profile in current_profile.friend_requests.all():
        current_profile.friends.add(sender_profile)
        sender_profile.friends.add(current_profile)

        current_profile.friend_requests.remove(sender_profile)
        messages.success(request, f"You are now friends with {sender.username}.")
    else:
        messages.warning(request, f"No friend request from {sender.username}.")

    return redirect('home')


@login_required
def reject_friend_request_view(request, user_id):
    sender = get_object_or_404(User, id=user_id)
    sender_profile = sender.profile
    current_profile = request.user.profile
    if sender_profile in current_profile.friend_requests.all():
        current_profile.friend_requests.remove(sender_profile)
        messages.success(request, f"Friend request from {sender.username} has been rejected.")
    else:
        messages.warning(request, f"No friend request from {sender.username}.")

    return redirect('home')


@login_required
def unfriend_view(request, user_id):
    target_user = get_object_or_404(User, id=user_id)

    current_user_profile = request.user.profile

    target_user_profile = target_user.profile

    if target_user_profile in current_user_profile.friends.all():
        current_user_profile.friends.remove(target_user_profile)
        target_user_profile.friends.remove(current_user_profile)
        messages.success(request, f"You are no longer friends with {target_user.username}.")
    else:
        messages.warning(request, f"{target_user.username} is not in your friends list.")

    return redirect('profile', user_id=target_user.id)



@login_required
def home_view(request):
    query = request.GET.get('q') 
    search_results = None
    if query:
        search_results = User.objects.filter(
            Q(username__icontains=query) | Q(email__icontains=query)
        )

    if request.method == 'POST' and 'create_post' in request.POST:
        post_form = PostForm(request.POST, request.FILES) 
        if post_form.is_valid():
            post = post_form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('home')
    else:
        post_form = PostForm()

    user_friends = request.user.profile.friends.all()
    posts = Post.objects.filter(author__profile__in=user_friends).exclude(author=request.user).order_by('-created_at')

    return render(request, 'core/home.html', {
        'posts': posts,
        'search_results': search_results,
        'query': query,
        'post_form': post_form,
    })


@login_required
def create_post_view(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('home')
    else:
        form = PostForm()
    return render(request, 'core/create_post.html', {'form': form})





@login_required
def post_detail_view(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = post.comments.all() 
    comment_form = CommentForm()
    return render(request, 'core/post_detail.html', {
        'post': post,
        'comments': comments,
        'comment_form': comment_form,
    })




@login_required
def add_comment_view(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    
    if request.method == 'POST':
        comment_content = request.POST.get('content')

        if not comment_content:
            return JsonResponse({'error': 'Content is required.'}, status=400)
        comment = Comment.objects.create(
            post=post,
            author=request.user,
            content=comment_content
        )
        return JsonResponse({
            'comment_author': comment.author.username,
            'comment_content': comment.content,
            'comment_created_at': comment.created_at.strftime('%b %d, %Y, %I:%M %p'),
            'post_id': post_id,
        })

    return JsonResponse({'error': 'Invalid request'}, status=400)

@login_required
def like_post_view(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.user in post.likes.all():
        post.likes.remove(request.user) 
        liked = False
    else:
        post.likes.add(request.user) 
        liked = True

    return JsonResponse({'liked': liked, 'like_count': post.likes.count()})





@login_required
def profile_view(request, user_id):
    profile = get_object_or_404(Profile, user_id=user_id)
    posts = Post.objects.filter(author=profile.user).order_by('-created_at')
    is_own_profile = (profile.user == request.user)

    if request.method == 'POST' and is_own_profile:
        form = ProfilePictureForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile picture updated successfully.')
            return redirect('profile', user_id=user_id)
    else:
        form = ProfilePictureForm(instance=profile)

    return render(request, 'core/profile.html', {
        'profile': profile,
        'posts': posts,
        'is_own_profile': is_own_profile,
        'form': form,
    })
