from django.forms import ModelForm
from .models import Post
from django.contrib.auth.models import User

class PostForm(ModelForm):
	class Meta:
		model = Post
		fields = ['author', 'title', 'context']

class BasePostForm(ModelForm):
	class Meta:
		model = Post
		fields = ['title', 'context']

class UserForm(ModelForm):
	class Meta:
		model = User
		fields = ['username', 'password']