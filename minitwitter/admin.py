from django.contrib import admin
from .models import Post, Member, Article, Photo

# Register your models here.
admin.site.register(Post)
admin.site.register(Member)
admin.site.register(Article)
admin.site.register(Photo)