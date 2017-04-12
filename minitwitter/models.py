from django.db import models
from django.utils import timezone

# Create your models here.
class Post(models.Model):
	author = models.CharField(max_length=40)
	title  = models.CharField(max_length=100)
	context = models.TextField()
	created_time = models.DateTimeField(auto_now=False, auto_now_add=True)
	modified_time = models.DateTimeField(auto_now=True)

	def __str__(self):
		return 'author: ' + self.author+ ', title: ' + self.title + ', context: ' + self.context