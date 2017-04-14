from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from .models import Post, Member, Article, Photo
from django.contrib.auth.models import User
from .forms import PostForm, BasePostForm, LoginUserForm, SigninUserForm, SigninUserModelForm, SigninMemberForm, SigninMemberModelForm,  PhotoForm, ArticleForm
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
	if request.method == 'GET':
		return HttpResponseRedirect(reverse('minitwitter:login'))
"""
def signin(request):
	if request.method == 'GET':
		form1 = SigninUserModelForm(prefix='form1_prefix')
		form2 = SigninMemberModelForm(prefix='form2_prefix')
		return render(request, 'minitwitter/signin.html', {'form': form1, 'form2':form2})
	if request.method == 'POST':
		form1 = SigninUserModelForm(request.POST, prefix='form1_prefix')
		if form1.is_valid():
			form1['password'] = form1.cleaned_data['password']
			input_user = form1.save()
			request.POST['form2_prefix-user']=User.objects.get(pk=input_user.id).id
			form2 = SigninMemberModelForm(request.POST, request.FILES, prefix='form2_prefix')
			if form2.is_valid():
				input_member = form2.save()
			else:
				print(form2.errors)
		else:
			print(form1.errors)
		return HttpResponseRedirect(reverse('minitwitter:index'))
"""
def signin(request):
	if request.method == 'GET':
		form1 = SigninUserForm(prefix='form1_prefix')
		form2 = SigninMemberForm(prefix='form2_prefix')
		return render(request, 'minitwitter/signin.html', {'form1': form1, 'form2':form2})
	if request.method == 'POST':
		form1 = SigninUserForm(request.POST, prefix='form1_prefix')
		if form1.is_valid():
			print('form1')
			print(form1)
			username=form1.cleaned_data['user_name']
			password=form1.cleaned_data['password']
			email=form1.cleaned_data['email']
			input_user = User(username=username, email=email)
			input_user.set_password(password)
			input_user.save()
			form2 = SigninMemberForm(request.POST, request.FILES, prefix='form2_prefix')
			print('form2')
			print(form2)
			if form2.is_valid():
				nickname=form2.cleaned_data['nickname']
				birthday=form2.cleaned_data['birthday']
				gender=form2.cleaned_data['gender']
				profile=form2.cleaned_data['profile']
				input_member = Member(user=input_user, nickname=nickname, birthday=birthday, gender=gender, profile=profile)
				input_member.save()
			else:
				print(form2.errors)
		else:
			print(form1.errors)
		return HttpResponseRedirect(reverse('minitwitter:index'))

def timeline(request):
	if request.method == 'GET':
		print(request.user)
		this_member = Member.objects.get(user=request.user)
		articles = Article.objects.all().order_by('-modified_time')
		photos = Photo.objects.all()
		return render(request, 'minitwitter/timeline.html', {'this_member': this_member, 'articles': articles, 'photos': photos})

def my_timeline(request):
	if request.method == 'GET':
		print(request.user)
		this_member = Member.objects.get(user=request.user)
		articles = Article.objects.filter(author=this_member).order_by('-modified_time')
	return render(request, 'minitwitter/timeline.html', {'this_member': this_member, 'articles': articles, 'flag': 'me'})

def write_article(request):
	if request.method == 'GET':
		form1 = ArticleForm(prefix='form1_prefix')
		form2 = PhotoForm(prefix='form2_prefix')
		return render(request, 'minitwitter/article.html', {'form1': form1, 'form2': form2})
	if request.method == 'POST':
		form1 = ArticleForm(request.POST, prefix='form1_prefix')
		if form1.is_valid():
			print('form1')
			print(form1)
			context=form1.cleaned_data['context']
			author = Member.objects.get(user=request.user)
			input_article = Article(author=author, context=context)
			input_article.save()
			form2 = PhotoForm(request.POST, request.FILES, prefix='form2_prefix')
			print('form2')
			print(form2)
			if form2.is_valid():
				photo=form2.cleaned_data['photo']
				print(photo)
				input_photo = Photo(article=input_article, photo=photo)
				input_photo.save()
			else:
				print(form2.errors)
		else:
			print(form1.errors)
		return HttpResponseRedirect(reverse('minitwitter:timeline'))

def modify_article(request, article_id):
	if request.method == "GET":
		this_article = Article.objects.get(id=article_id)
		these_photos = Photo.objects.filter(article_id=article_id)
		form1 = ArticleForm({'context': this_article.context})
		form2 = PhotoForm({'photo': these_photos})
		return render(request, 'minitwitter/article.html', {'form1': form1, 'form2': form2})
	if request.method == "POST":
		form1 = ArticleForm(request.POST)
		if form1.is_valid():
			print('form1')
			print(form1)
			this_article = Article.objects.get(id=article_id)
			context=form1.cleaned_data['context']
			this_article.context = context
			this_article.save()
			form2 = PhotoForm(request.FILES)
			print('form2')
			print(form2)
			if form2.is_valid():
				print('OK')
			else:
				print(form2.errors)
		else:
			print(form1.errors)
		return HttpResponseRedirect(reverse('minitwitter:timeline'))

def uploads(request, file):
	if file[0:8] == 'profile/':
		member = Member.objects.get(profile=file)
		return HttpResponse(member.profile)
	if file[0:6] == 'media/':
		photos = Photo.objects.get(photo=file)
		return HttpResponse(photos.photo)
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
		