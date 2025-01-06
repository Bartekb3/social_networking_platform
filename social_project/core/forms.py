from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Post, Comment 

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)  # Email field
    first_name = forms.CharField(max_length=30, required=True)  # First name
    last_name = forms.CharField(max_length=30, required=True)  # Last name

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']

class CommentForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea, max_length=250, label="Write a comment")

    class Meta:
        model = Comment
        fields = ['content']

class PostForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea, max_length=500, label="Write a post")

    class Meta:
        model = Post
        fields = ['content']