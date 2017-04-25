from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from .models import Post, Member, Article, Photo, Hashtag, Tagged
from django.contrib.auth.models import User
from .forms import LoginUserForm, SigninUserForm, SigninMemberForm, PhotoForm
from .forms import ArticleForm, ModifyMemberForm, HashtagForm
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate
from django.conf import settings
from django.views import View
from django.contrib import messages
import os
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.db import transaction
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.
@transaction.non_atomic_requests
def index(request):
	return HttpResponseRedirect(reverse('minitwitter:login'))


class SigninView(View):
	template_name = 'minitwitter/signin.html'

	@transaction.non_atomic_requests
	def get(self, request):
		form1 = SigninUserForm(prefix='form1_prefix')
		form2 = SigninMemberForm(prefix='form2_prefix')
		context = {'form1': form1, 'form2':form2}
		return render(request, self.template_name, context)
	
	@transaction.atomic
	def post(self, request):
		form1 = SigninUserForm(request.POST, prefix='form1_prefix')
		form2 = SigninMemberForm(request.POST, request.FILES, prefix='form2_prefix')
		context = {'form1': form1, 'form2':form2}
		if form1.is_valid():
			if form2.is_valid():
				username=form1.cleaned_data['user_name']
				password=form1.cleaned_data['password']
				email=form1.cleaned_data['email']
				input_user = User(username=username, email=email)
				input_user.set_password(password)
				input_user.save()

				nickname=form2.cleaned_data['nickname']
				birthday=form2.cleaned_data['birthday']
				gender=form2.cleaned_data['gender']
				profile=form2.cleaned_data['profile']
				input_member = Member(user=input_user, nickname=nickname, 
					birthday=birthday, gender=gender, profile=profile)
				input_member.save()
				return HttpResponseRedirect(reverse('minitwitter:index'))
			else:
				messages.error(request, form2.errors.as_json())
				return render(request, self.template_name, context)
		else:
			messages.error(request, form2.errors.as_json())
			return render(request, self.template_name, context)
"""
def signin(request):
	if request.method == 'GET':
		form1 = SigninUserForm(prefix='form1_prefix')
		form2 = SigninMemberForm(prefix='form2_prefix')
		return render(request, 'minitwitter/signin.html', {'form1': form1, 'form2':form2})
	if request.method == 'POST':
		form1 = SigninUserForm(request.POST, prefix='form1_prefix')
		if form1.is_valid():
			username=form1.cleaned_data['user_name']
			password=form1.cleaned_data['password']
			email=form1.cleaned_data['email']
			input_user = User(username=username, email=email)
			input_user.set_password(password)
			input_user.save()
			form2 = SigninMemberForm(request.POST, request.FILES, prefix='form2_prefix')
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
		return HttpResponseRedirect(reverse('minitwitter:index'))"""

#@login_required
class TimelineView(View):
	template_name = 'minitwitter/timeline.html'

	@method_decorator(login_required)
	@transaction.non_atomic_requests
	def get(self, request):
		this_member = Member.objects.get(user=request.user)
		article_list = Article.objects.all().order_by('-modified_time')
		paginator = Paginator(article_list, 10)

		page = request.GET.get('page')
		try:
			articles = paginator.page(page)
		except PageNotAnInteger:
			articles = paginator.page(1)
		except EmptyPage:
			articles = paginator.page(paginator.num_pages)
		context = {'this_member': this_member, 'articles': articles }
		return render(request, self.template_name, context)
"""
def timeline(request):
	if request.method == 'GET':
		this_member = Member.objects.get(user=request.user)
		articles = Article.objects.all().order_by('-modified_time')
		photos = Photo.objects.all()
		tags = Tagged.objects.all()
		return render(request, 'minitwitter/timeline.html', {'this_member': this_member, 'articles': articles, 'photos': photos, 'tagged': tags})
"""

class MyTimelineView(View):
	template_name = 'minitwitter/timeline.html'

	@method_decorator(login_required)
	@transaction.non_atomic_requests
	def get(self, request):
		this_member = Member.objects.get(user=request.user)
		article_list = Article.objects.filter(author=this_member).order_by('-modified_time')
		paginator = Paginator(article_list, 10)

		page = request.GET.get('page')
		try:
			articles = paginator.page(page)
		except PageNotAnInteger:
			articles = paginator.page(1)
		except EmptyPage:
			articles = paginator.page(paginator.num_pages)
		context = {'this_member': this_member, 
				   'articles': articles, 'flag': 'me'}
		return render(request, self.template_name, context)

"""@login_required
def my_timeline(request):
	if request.method == 'GET':
		this_member = Member.objects.get(user=request.user)
		articles = Article.objects.filter(author=this_member).order_by('-modified_time')
		photos = Photo.objects.all()
		tags = Tagged.objects.all()
		return render(request, 'minitwitter/timeline.html', {'this_member': this_member, 'articles': articles, 'photos': photos, 'tagged': tags, 'flag': 'me'})
"""

class WriteArticleView(View):
	template_name = 'minitwitter/article.html'
	
	@method_decorator(login_required)
	@transaction.non_atomic_requests
	def get(self, request):
		form1 = ArticleForm(prefix='form1_prefix')
		form2 = PhotoForm(prefix='form2_prefix')
		form3 = HashtagForm(prefix='form3_prefix')
		context = {'form1': form1, 'form2': form2, 'form3': form3}
		return render(request, self.template_name, context)
	
	@method_decorator(login_required)
	@transaction.atomic
	def post(self, request):
		form1 = ArticleForm(request.POST, prefix='form1_prefix')
		form2 = PhotoForm(request.POST, request.FILES, prefix='form2_prefix')
		context = {'form1': form1, 'form2':form2}
		if form1.is_valid():
			if form2.is_valid():
				context=form1.cleaned_data['context']
				author = Member.objects.get(user=request.user)
				input_article = Article(author=author, context=context)
				input_article.save()
			
				files = request.FILES.getlist('form2_prefix-photo')
				for file in files:
					input_photo = Photo(article=input_article, photo=file)
					input_photo.save()
				hashtags = request.POST['hashtag_field']
				hashtags_array = hashtags.split('  ')
				"""initial_offset = 0
				last_offset = 0
				i = 0
				print(len(hashtags))
				while last_offset < len(hashtags):
					print(initial_offset)
					try:
						initial_offset = hashtags.index('#', initial_offset)
						last_offset = hashtags.index('  ', initial_offset)
					except ValueError:
						last_offset = len(hashtags)
					else:
						current_hashtag = hashtags[initial_offset:last_offset]
						input_hashtag = Hashtag.objects.filter(hashtag=current_hashtag)
						if input_hashtag:
							input_hashtag = input_hashtag[0]
							input_hashtag.counts += 1
						else:
							input_hashtag = Hashtag(hashtag=current_hashtag)
						input_hashtag.save()
						Tagged(article=input_article, hashtag=input_hashtag).save()

						print(hashtags[initial_offset:last_offset])
						initial_offset += last_offset - initial_offset
				return HttpResponseRedirect(reverse('minitwitter:timeline'))
				"""
				for i in range(len(hashtags_array) - 1):
					if hashtags_array[i][0] == '#':
						hashtag, created = Hashtag.objects.get_or_create(hashtag=hashtags_array[i])
						hashtag.counts += 1
						hashtag.save()
						Tagged(article=input_article, hashtag=hashtag).save()
					else:
						pass
				return HttpResponseRedirect(reverse('minitwitter:timeline'))
			else:
				print(form2.errors)
				return render(request, self.template_name, context)
		else:
			print(form1.errors)
			return render(request, self.template_name, context)
"""		
@login_required
def write_article(request):
	if request.method == 'GET':
		form1 = ArticleForm(prefix='form1_prefix')
		form2 = PhotoForm(prefix='form2_prefix')
		form3 = HashtagForm(prefix='form3_prefix')
		return render(request, 'minitwitter/article.html', {'form1': form1, 'form2': form2, 'form3': form3})
	if request.method == 'POST':
		print(request.POST)
		form1 = ArticleForm(request.POST, prefix='form1_prefix')
		if form1.is_valid():
			context=form1.cleaned_data['context']
			author = Member.objects.get(user=request.user)
			input_article = Article(author=author, context=context)
			input_article.save()
			form2 = PhotoForm(request.POST, request.FILES, prefix='form2_prefix')
			files = request.FILES.getlist('form2_prefix-photo')
			if form2.is_valid():
				for file in files:
					input_photo = Photo(article=input_article, photo=file)
					input_photo.save()
				hashtags = request.POST['hashtag_field']
				initial_offset = 0
				last_offset = 0
				i = 0
				print(len(hashtags))
				while last_offset < len(hashtags):
					print(initial_offset)
					try:
						initial_offset = hashtags.index('#', initial_offset)
						last_offset = hashtags.index('  ', initial_offset)
					except ValueError:
						last_offset = len(hashtags)
					else:
						current_hashtag = hashtags[initial_offset:last_offset]
						input_hashtag = Hashtag.objects.filter(hashtag=current_hashtag)
						if input_hashtag:
							input_hashtag = input_hashtag[0]
							input_hashtag.counts += 1
						else:
							input_hashtag = Hashtag(hashtag=current_hashtag)
						input_hashtag.save()
						new_tagged = Tagged(article=input_article, hashtag=input_hashtag)
						new_tagged.save()

						print(hashtags[initial_offset:last_offset])
						initial_offset += last_offset - initial_offset
			else:
				print(form2.errors)
		else:
			print(form1.errors)
		return HttpResponseRedirect(reverse('minitwitter:timeline'))
"""
class ModifyArticleView(View):
	template_name = 'minitwitter/article.html'

	@method_decorator(login_required)
	@transaction.non_atomic_requests
	def get(self, request, *args, **kwargs):
		article_id = kwargs['article_id']
		this_article = Article.objects.get(id=article_id)
		
		form1 = ArticleForm({'context': this_article.context})
		form2 = PhotoForm()
		form3 = HashtagForm(prefix='form3_prefix')
		context = {'form1': form1, 'form2': form2, 'form3': form3, 'article': this_article }
		return render(request, self.template_name, context)
	
	@method_decorator(login_required)
	@transaction.atomic
	def post(self, request, *args, **kwargs):
		form1 = ArticleForm(request.POST)
		form2 = PhotoForm(request.POST, request.FILES)
		article_id = kwargs['article_id']
		context = {'form1': form1, 'form2':form2}
		if form1.is_valid():
			if form2.is_valid():
				this_article = Article.objects.get(id=article_id)
				context=form1.cleaned_data['context']
				this_article.context = context
				this_article.save()
				
				files = request.FILES.getlist('photo')
				for file in files:
					input_photo = Photo(article=this_article, photo=file)
					input_photo.save()
				hashtags = request.POST['hashtag_field']
				hashtags_array = hashtags.split('  ')
				"""initial_offset = 0
				last_offset = 0
				i = 0
				existing_hashtags = Tagged.objects.filter(article=this_article)
				while last_offset < len(hashtags):
					try:
						initial_offset = hashtags.index('#', initial_offset)
						last_offset = hashtags.index('  ', initial_offset)
					except ValueError:
						last_offset = len(hashtags)
					else:
						current_hashtag = hashtags[initial_offset:last_offset]
						existing_flag = 0
						for existing_hashtag in existing_hashtags:
							if existing_hashtag.hashtag.hashtag != current_hashtag:
								pass
							else:
								existing_flag = 1
								break
						if existing_flag == 0:
							input_hashtag = Hashtag.objects.filter(hashtag=current_hashtag)
							if input_hashtag:
								input_hashtag = input_hashtag[0]
								input_hashtag.counts += 1
							else:
								input_hashtag = Hashtag(hashtag=current_hashtag)
							input_hashtag.save()
							Tagged(article=this_article, hashtag=input_hashtag).save()
						initial_offset += last_offset - initial_offset"""
				for i in range(len(hashtags_array) - 1):
					if hashtags_array[i][0] == '#':
						hashtag, tag_created = Hashtag.objects.get_or_create(hashtag=hashtags_array[i])
						tagged, tagged_created = Tagged.objects.get_or_create(hashtag=hashtag, article =this_article)
						if tag_created or tagged_created:
							hashtag.counts += 1
						hashtag.save()
					else:
						pass
				return HttpResponseRedirect(reverse('minitwitter:timeline'))
			else:
				print(form2.errors)
				return render(request, self.template_name, context)
		else:
			print(form1.errors)
			return render(request, self.template_name, context)
		
"""	
@login_required
def modify_article(request, article_id):
	if request.method == "GET":
		this_article = Article.objects.get(id=article_id)
		these_photos = Photo.objects.filter(article_id=article_id)
		photos_list = []
		form1 = ArticleForm({'context': this_article.context})
		if len(these_photos) == 0:
			form2 = PhotoForm()
		else:
			for this_photo in these_photos:
				form2 = PhotoForm()
				photos_list.append({'id': this_photo.id, 'photo': this_photo.photo})
		tagged = Tagged.objects.filter(article_id=article_id)
		these_hashtags = ""
		for item in tagged:
			these_hashtags += item.hashtag.hashtag+"  "
		form3 = HashtagForm(prefix='form3_prefix')
		return render(request, 'minitwitter/article.html', {'form1': form1, 'form2': form2, 'form3': form3, 'these_photos': photos_list, 'these_hashtags': these_hashtags})
		
	if request.method == "POST":
		form1 = ArticleForm(request.POST)
		print(request.POST)
		print(request.FILES)
		if form1.is_valid():
			this_article = Article.objects.get(id=article_id)
			context=form1.cleaned_data['context']
			this_article.context = context
			this_article.save()
			form2 = PhotoForm(request.POST, request.FILES)
			files = request.FILES.getlist('photo')
			if form2.is_valid():
				for file in files:
					input_photo = Photo(article=this_article, photo=file)
					input_photo.save()
				hashtags = request.POST['hashtag_field']
				initial_offset = 0
				last_offset = 0
				i = 0
				existing_hashtags = Tagged.objects.filter(article=this_article)
				print(len(hashtags))
				while last_offset < len(hashtags):
					print('initial_offset')
					print(initial_offset)
					try:
						initial_offset = hashtags.index('#', initial_offset)
						last_offset = hashtags.index('  ', initial_offset)
					except ValueError:
						last_offset = len(hashtags)
					else:
						current_hashtag = hashtags[initial_offset:last_offset]
						existing_flag = 0
						for existing_hashtag in existing_hashtags:
							if existing_hashtag.hashtag.hashtag != current_hashtag:
								print("not existing: "+current_hashtag)
							else:
								print("existing: "+existing_hashtag.hashtag.hashtag)
								existing_flag = 1
								break
						print('existing_flag')
						print(existing_flag)
						if existing_flag == 0:
							input_hashtag = Hashtag.objects.filter(hashtag=current_hashtag)
							print('input_hashtag')
							print(input_hashtag)
							if input_hashtag:
								input_hashtag = input_hashtag[0]
								print('exists')
								input_hashtag.counts += 1
							else:
								print('not exists')
								input_hashtag = Hashtag(hashtag=current_hashtag)
							input_hashtag.save()
							print(input_hashtag)
							new_tagged = Tagged(article=this_article, hashtag=input_hashtag)
							new_tagged.save()
						print('hashtag')
						print(hashtags[initial_offset:last_offset])
						initial_offset += last_offset - initial_offset
				else:
					pass
			else:
				print(form2.errors)
		else:
			print(form1.errors)
		return HttpResponseRedirect(reverse('minitwitter:timeline'))
"""
class ModifyUserView(View):
	template_name = 'minitwitter/modifyuserinfo.html'

	@method_decorator(login_required)
	@transaction.non_atomic_requests
	def get(self, request):
		this_member = Member.objects.get(user=request.user)
		initial_context = {'nickname': this_member.nickname,
						   'profile': this_member.profile ,
		 				   'birthday': this_member.birthday,
		 				   'gender': this_member.gender}
		form = ModifyMemberForm(initial=initial_context)	
		context = {'form': form}
		return render(request, self.template_name, context)

	@method_decorator(login_required)
	@transaction.atomic
	def post(self, request):
		form = ModifyMemberForm(request.POST, request.FILES)
		context = {'form': form}
		if form.is_valid():
			this_member = Member.objects.get(user=request.user)
			nickname=form.cleaned_data['nickname']
			birthday=form.cleaned_data['birthday']
			gender=form.cleaned_data['gender']
			if request.FILES:
				profile_path = this_member.profile
				os.remove(os.path.join(settings.MEDIA_ROOT, str(profile_path)))
				profile=form.cleaned_data['profile']
			else:
				profile=this_member.profile
			this_member.nickname=nickname
			this_member.birthday=birthday
			this_member.gender=gender
			this_member.profile=profile
			this_member.save()
			return HttpResponseRedirect(reverse('minitwitter:timeline'))
		else:
			print(form.errors)	
			return render(request, self.template_name, context)
"""
@login_required
def modify_user(request):
	if request.method == "GET":
		this_member = Member.objects.get(user=request.user)
		form = ModifyMemberForm(initial={'nickname': this_member.nickname, 'profile': this_member.profile , 'birthday': this_member.birthday, 'gender': this_member.gender})	
		return render(request, 'minitwitter/modifyuserinfo.html', {'form': form})
	if request.method == "POST":
		form = ModifyMemberForm(request.POST, request.FILES)
		if form.is_valid():
			this_member = Member.objects.get(user=request.user)
			nickname=form.cleaned_data['nickname']
			birthday=form.cleaned_data['birthday']
			gender=form.cleaned_data['gender']
			if request.FILES:
				profile_path = this_member.profile
				os.remove(os.path.join(settings.MEDIA_ROOT, str(profile_path)))
				profile=form.cleaned_data['profile']
			else:
				profile=this_member.profile
			this_member.nickname=nickname
			this_member.birthday=birthday
			this_member.gender=gender
			this_member.profile=profile
			this_member.save()
		else:
			print(form.errors)	
	return HttpResponseRedirect(reverse('minitwitter:timeline'))
"""
@transaction.non_atomic_requests
def uploads(request, file):
	if file[0:8] == 'profile/':
		member = Member.objects.get(profile=file)
		return HttpResponse(member.profile)
	if file[0:6] == 'media/':
		photos = Photo.objects.get(photo=file)
		return HttpResponse(photos.photo)

@login_required
@transaction.atomic
def delete_image(request, photo_id):
	photo = Photo.objects.get(id=photo_id)
	photo_path = photo.photo
	photo.delete();
	os.remove(os.path.join(settings.MEDIA_ROOT, str(photo_path)))
	return HttpResponse("")

@transaction.non_atomic_requests
def check_user_name(request, user_name):
	try:
		user = User.objects.get(username=user_name)
	except User.DoesNotExist:
		return HttpResponse("You can use that User Name.")
	else:
		return HttpResponse("You can't use that User Name.", status=409)

@transaction.non_atomic_requests
def check_nickname(request, nickname):
	try:
		member = Member.objects.get(nickname=nickname)
	except Member.DoesNotExist:
		return HttpResponse("You can use that Nickname.")
	else:
		return HttpResponse("You can't use that Nickname.", status=409)

class SearchArticleView(View):
	template_name = 'minitwitter/timeline.html'
	
	@method_decorator(login_required)
	@transaction.non_atomic_requests
	def get(self, request, *args, **kwargs):
		this_member = Member.objects.get(user=request.user)
		hashtag = Hashtag.objects.get(hashtag=kwargs['hashtag'])
		tagged_articles = Tagged.objects.filter(hashtag=hashtag).order_by('-modified_time')
		article_list = []
		for tagged_article in tagged_articles:
			article_list.append(tagged_article.article)

		paginator = Paginator(article_list, 5)

		page = request.GET.get('page')
		try:
			articles = paginator.page(page)
		except PageNotAnInteger:
			articles = paginator.page(1)
		except EmptyPage:
			articles = paginator.page(paginator.num_pages)

		context = {'this_member': this_member, 'articles': articles}
		return render(request, self.template_name, context)
"""
@login_required
def search_article(request, hashtag):
	this_member = Member.objects.get(user=request.user)
	hashtag = Hashtag.objects.get(hashtag=hashtag)
	tagged_articles = Tagged.objects.filter(hashtag=hashtag).order_by('-modified_time')
	articles = []
	for tagged_article in tagged_articles:
		articles.append(tagged_article.article)
	print(articles)
	print(tagged_articles)
	print(tagged_articles[0].article)
	photos = Photo.objects.all()
	tags = Tagged.objects.all()
	return render(request, 'minitwitter/timeline.html', {'this_member': this_member, 'articles': articles, 'photos': photos, 'tagged': tags})
"""
