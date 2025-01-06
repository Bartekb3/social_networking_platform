from django.urls import path
from django.contrib.auth.views import LogoutView, LoginView
from .views import signup_view, CustomLoginView, CustomLogoutView, home_view,create_post_view,post_detail_view, add_comment_view, like_post_view, add_friend_view,profile_view
ethod_names = ['get', 'post', 'head', 'options'] 

urlpatterns = [
    path('', home_view, name='home'), # Homepage    
    path('signup/', signup_view, name='signup'),
     path('login/', LoginView.as_view(template_name='core/login.html'), name='login'),  # Login route
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),  # Redirect to login page after logout
    path('create_post/', create_post_view, name='create_post'),
    path('post/<int:post_id>/', post_detail_view, name='post_detail'),
    path('post/<int:post_id>/comment/', add_comment_view, name='add_comment'),
    path('post/<int:post_id>/like/', like_post_view, name='like_post'),
     path('user/<int:user_id>/add_friend/', add_friend_view, name='add_friend'),
     path('user/<int:user_id>/', profile_view, name='profile'),
]
