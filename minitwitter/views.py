from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from .models import Post
from .forms import PostForm
from django.http import HttpResponseRedirect, HttpResponse

# Create your views here.
def index(request):
	if request.method == 'GET':
		form = PostForm()
		return render(request, 'minitwitter/base.html', {'form': form})
	if request.method == 'POST':
		form = PostForm(request.POST)
		if form.is_valid():
			form.save()
		return HttpResponseRedirect(reverse('minitwitter:list'))

def list(request):
	posts = Post.objects.all()
	return render(request, 'minitwitter/list.html', {'posts': posts})

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
