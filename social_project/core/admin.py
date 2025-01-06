from django.contrib import admin
from .models import Post, Comment, Profile

# Register Post model
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('author', 'content', 'created_at')  # Columns to display in the admin interface
    list_filter = ('created_at',)  # Add filtering options
    search_fields = ('author__username', 'content')  # Add search functionality

# Register Comment model
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'author', 'content', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('author__username', 'content')

# Register Profile model
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user',)  # Display only the user field
    search_fields = ('user__username',)
