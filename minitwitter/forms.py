from django.forms import ModelForm, Form
from django import forms
from .models import Post, Member, Article, Photo
from django.contrib.auth.models import User

class PostForm(ModelForm):
	class Meta:
		model = Post
		fields = ['author', 'title', 'context']

class BasePostForm(ModelForm):
	class Meta:
		model = Post
		fields = ['title', 'context']

class LoginUserForm(ModelForm):
	class Meta:
		model = User
		fields = ['username', 'password']

class SigninUserForm(forms.Form):
	user_name = forms.CharField(label='User name', max_length=150)
	password = forms.CharField(label='Password', max_length=128, widget=forms.PasswordInput)
	password_check = forms.CharField(label='Password Check', max_length=128, widget=forms.PasswordInput)
	email = forms.CharField(label='Email', max_length=254, widget=forms.EmailInput)

class SigninUserModelForm(ModelForm):
	class Meta:
		model = User
		fields = ['username', 'password', 'email']
		widgets = {
			'password': forms.PasswordInput,
		}

class SigninMemberForm(forms.Form):
	GENDER_CHOICES = (
		('F', 'Female'),
		('M', 'Male'),
	)
	nickname = forms.CharField(label='Nickname', max_length=20)
	birthday = forms.DateField(label='Birthday')
	gender = forms.ChoiceField(label='Gender', choices=GENDER_CHOICES, widget=forms.Select)
	profile = forms.ImageField(label='Profile')

class SigninMemberModelForm(ModelForm):
	class Meta:
		model = Member
		fields = ['user', 'nickname', 'birthday', 'gender', 'profile']
		widgets = {
			'user': forms.HiddenInput,
		}

class ArticleForm(forms.Form):
	context = forms.CharField(label='Context', max_length=1000, widget=forms.Textarea(attrs={'cols':80, 'rows':10, 'autofocus':True}))

class PhotoForm(forms.Form):
	photo = forms.ImageField(label='Photo', required=False)

class ArticleModelForm(ModelForm):
	class Meta:
		model = Article
		fields = '__all__'



class PhotoModelForm(ModelForm):
	class Meta:
		model = Photo
		fields = ['photo']
