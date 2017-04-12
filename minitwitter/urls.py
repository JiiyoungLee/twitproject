from django.conf.urls import url
from django.contrib.auth import views as auth_views
from minitwitter import views

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^list/$', views.list, name='list'),
	url(r'^modify/(?P<post_id>\d+)/$', views.modify, name='modify'),
]
