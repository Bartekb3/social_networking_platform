from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Post model
class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)  # Reference to the User model
    content = models.TextField()  # Text content of the post
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp when the post is created
    likes = models.ManyToManyField(User, related_name='liked_posts', blank=True)  # Users who liked the post

    def __str__(self):
        return f"{self.author.username}'s Post on {self.created_at.strftime('%Y-%m-%d')}"

# Comment model
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')  # Reference to the related post
    author = models.ForeignKey(User, on_delete=models.CASCADE)  # Reference to the User model
    content = models.TextField()  # Text content of the comment
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp when the comment is created

    def __str__(self):
        return f"Comment by {self.author.username} on {self.created_at.strftime('%Y-%m-%d')}"

# Profile model
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    friends = models.ManyToManyField('self', symmetrical=True, blank=True)
    friend_requests = models.ManyToManyField('self', symmetrical=False, blank=True, related_name='pending_requests')

    def __str__(self):
        return f"{self.user.username}'s Profile"



@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

