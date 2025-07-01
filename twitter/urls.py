from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView
from django.conf import settings
from django.conf.urls.static import static
from .views import CustomLoginView  



urlpatterns = [
	path('', views.home, name='home'),
	path('register/', views.register, name='register'),
	path('login/', CustomLoginView.as_view(), name='login'),
	path('logout/', LogoutView.as_view(), name='logout'),
	path('delete/<int:post_id>/', views.delete, name='delete'),
	path('profile/<str:username>/', views.profile, name='profile'),
	path('editar/', views.editar, name='editar'),
	path('follow/<str:username>/', views.follow, name='follow'),
	path('unfollow/<str:username>/', views.unfollow, name='unfollow'),
 	path('like/<int:post_id>/', views.like_post, name='like_post'),
  path('repost/<int:post_id>/', views.repost, name='repost'),
	path('comment/<int:post_id>/', views.comment_post, name='comment_post'),
 path('post/<int:post_id>/comments/', views.post_comments, name='post_comments'),
path('post/<int:post_id>/reposts/', views.post_reposts, name='post_reposts'),



] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)