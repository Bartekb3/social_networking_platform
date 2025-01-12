from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Post, Comment , Profile

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    birthdate = forms.DateField(
        widget=forms.SelectDateWidget(years=range(1900, 2025)), 
        required=True
    )
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ]
    gender = forms.ChoiceField(choices=GENDER_CHOICES, widget=forms.RadioSelect, required=True)

    class Meta:
        model = User
        fields = [
            'username', 'email', 'first_name', 'last_name', 
            'birthdate', 'gender', 'password1', 'password2'
        ]

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            # Update the automatically created Profile with extra data
            profile = user.profile
            profile.birthdate = self.cleaned_data['birthdate']
            profile.gender = self.cleaned_data['gender']
            profile.save()
        return user

class CommentForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea, max_length=250, label="Write a comment")

    class Meta:
        model = Comment
        fields = ['content']

# class PostForm(forms.ModelForm):
#     content = forms.CharField(widget=forms.Textarea, max_length=500, label="Write a post")

#     class Meta:
#         model = Post
#         fields = ['content']
# forms.py

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content', 'image']  # Include 'image' here

class ProfilePictureForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_picture']