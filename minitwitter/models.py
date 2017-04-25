from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.

class Member(models.Model):
	GENDERCHOICE = (
		('F', 'Female'),
		('M', 'Male'),
	)

	user = models.OneToOneField(User)
	nickname = models.CharField(max_length=20)
	birthday = models.DateField(auto_now=False, auto_now_add=False, blank=True)
	gender = models.CharField(max_length=1, choices=GENDERCHOICE)
	profile = models.ImageField(upload_to='profile/')
	modified_time = models.DateTimeField(auto_now=True)

	def __str__(self):
		return 'id: ' + self.user.username + ', email: ' + self.user.email

class Article(models.Model):
	author = models.ForeignKey(Member)
	context = models.CharField(max_length=1000)
	created_time = models.DateTimeField(auto_now=False, auto_now_add=True)
	modified_time = models.DateTimeField(auto_now=True)

	def __str__(self):
		return "author: " + self.author.nickname + ", context: " + self.context

class Photo(models.Model):
	article = models.ForeignKey(Article)
	photo = models.ImageField(upload_to='media/')
	created_time = models.DateTimeField(auto_now=False, auto_now_add=True)
	modified_time = models.DateTimeField(auto_now=True)

	def __str__(self):
		return "article: " + self.article.context

class Hashtag(models.Model):
	hashtag = models.CharField(max_length=40)
	counts = models.IntegerField(default=0)
	created_time = models.DateTimeField(auto_now=False, auto_now_add=True)
	modified_time = models.DateTimeField(auto_now=True)

	def __str__(self):
		return "hashtag: " + self.hashtag

class Tagged(models.Model):
	article = models.ForeignKey(Article)
	hashtag = models.ForeignKey(Hashtag)
	created_time = models.DateTimeField(auto_now=False, auto_now_add=True)
	modified_time = models.DateTimeField(auto_now=True)

#test code
class Post(models.Model):
	author = models.CharField(max_length=40)
	title  = models.CharField(max_length=100)
	context = models.TextField()
	created_time = models.DateTimeField(auto_now=False, auto_now_add=True)
	modified_time = models.DateTimeField(auto_now=True)

	def __str__(self):
		return 'author: ' + self.author+ ', title: ' + self.title + ', context: ' + self.context