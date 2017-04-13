from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from .models import Post
from .forms import PostForm, UserForm, BasePostForm
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
	if request.method == 'GET':
		return HttpResponseRedirect(reverse('minitwitter:login'))

#test code	
@login_required(login_url='/test/auth/login/')
def list(request):
	posts = Post.objects.all()
	return render(request, 'minitwitter/list.html', {'posts': posts})

@login_required(login_url='/test/auth/login/')
def modify(request, post_id):
	this_post = Post.objects.get(pk=post_id)
	if request.method == 'GET':
		form = PostForm(instance=this_post)
		return render(request, 'minitwitter/base.html', {'form': form, 'form_id': post_id})
	if request.method == 'POST':
		form = PostForm(request.POST, instance=this_post)
		if form.is_valid():
			form.save()
		return HttpResponseRedirect(reverse('minitwitter:list'))

@login_required(login_url='/test/auth/login/')
def write(request):
	if request.method == 'GET':
		form = BasePostForm()
		return render(request, 'minitwitter/base.html', {'form': form, 'username': request.user.username})
	if request.method == 'POST':
		form = PostForm(request.POST)
		if form.is_valid():
			form.save()
		return HttpResponseRedirect(reverse('minitwitter:list'))
		