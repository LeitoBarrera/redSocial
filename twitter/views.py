from django.shortcuts import render, redirect
from .models import Profile, Post, Relationship, Like, Repost, Comment
from .forms import UserRegisterForm, PostForm, ProfileUpdateForm, UserUpdateForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView



@login_required
def home(request):
	posts = Post.objects.all()
	if request.method == 'POST':
		form = PostForm(request.POST)
		if form.is_valid():
			post = form.save(commit=False)
			post.user = request.user
			post.save()
			return redirect('home')
	else:
		form = PostForm()

	context = {'posts':posts, 'form' : form }
	return render(request, 'twitter/newsfeed.html', context)

def register(request):
	if request.method == 'POST':
		form = UserRegisterForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('home')
	else:
		form = UserRegisterForm()

	context = {'form' : form}
	return render(request, 'twitter/register.html', context)


def delete(request, post_id):
	post = Post.objects.get(id=post_id)
	post.delete()
	return redirect('home')


def profile(request, username):
    perfil_usuario = User.objects.get(username=username)
    posts = perfil_usuario.posts.all()
    context = {'perfil_usuario': perfil_usuario, 'posts': posts}
    return render(request, 'twitter/profile.html', context)


@login_required
def editar(request):
	if request.method == 'POST':
		u_form = UserUpdateForm(request.POST, instance=request.user)
		p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

		if u_form.is_valid() and p_form.is_valid():
			u_form.save()
			p_form.save()
			return redirect('home')
	else:
		u_form = UserUpdateForm(instance=request.user)
		p_form = ProfileUpdateForm()

	context = {'u_form' : u_form, 'p_form' : p_form}
	return render(request, 'twitter/editar.html', context)

@login_required
def follow(request, username):
	current_user = request.user
	to_user = User.objects.get(username=username)
	to_user_id = to_user
	rel = Relationship(from_user=current_user, to_user=to_user_id)
	rel.save()
	return redirect('home')

@login_required
def unfollow(request, username):
	current_user = request.user
	to_user = User.objects.get(username=username)
	to_user_id = to_user.id
	rel = Relationship.objects.get(from_user=current_user.id, to_user=to_user_id)
	rel.delete()
	return redirect('home')

@login_required
def like_post(request, post_id):
    post = Post.objects.get(id=post_id)
    like, created = Like.objects.get_or_create(user=request.user, post=post)
    if not created:
        like.delete()  # toggle like
    return redirect('home')


@login_required
def repost(request, post_id):
    post = Post.objects.get(id=post_id)
    repost, created = Repost.objects.get_or_create(user=request.user, post=post)
    if not created:
        repost.delete() 
    else:
        Post.objects.create(user=request.user, content=post.content)
    return redirect('home')

@login_required
def comment_post(request, post_id):
    post = Post.objects.get(id=post_id)
    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            Comment.objects.create(user=request.user, post=post, content=content)
    return redirect('home')
  
@login_required
def post_comments(request, post_id):
    post = Post.objects.get(id=post_id)
    comments = Comment.objects.filter(post=post).order_by('-timestamp')
    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            Comment.objects.create(user=request.user, post=post, content=content)
            return redirect('post_comments', post_id=post_id)
    return render(request, 'twitter/post_comments.html', {'post': post, 'comments': comments})


@login_required
def post_reposts(request, post_id):
    post = Post.objects.get(id=post_id)
    if post.user != request.user:
        return redirect('home')
    reposts = Repost.objects.filter(post=post)
    return render(request, 'twitter/post_reposts.html', {'post': post, 'reposts': reposts})


class CustomLoginView(LoginView):
    template_name = 'twitter/login.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['hide_navbar'] = True 
        return context

















