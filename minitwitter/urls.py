from django.conf.urls import url, include
from django.contrib.auth import views as auth_views
from minitwitter import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^auth/', include('django.contrib.auth.urls')),
	url(r'^signin/$', views.signin, name='signin'),
	url(r'^timeline/$', views.timeline, name='timeline'),
	url(r'^timeline/me$', views.my_timeline, name='my_timeline'),
	url(r'^articles/write$', views.write_article, name='write_article'),
	url(r'^articles/modify/(?P<article_id>\d+)/$', views.modify_article, name='modify_article'),
	url(r'^uploads/(?P<file>.+)', views.uploads, name='upload'),
	url(r'^modify/me', views.modify_user, name='modify_user'),
	url(r'^delete/image/(?P<photo_id>\d+)', views.delete_image, name='delete_image'),
	url(r'^auth/check/username/(?P<user_name>.+)', views.check_user_name, name='check_username'),
	url(r'^auth/check/nickname/(?P<nickname>.+)', views.check_nickname, name='check_nickname'),


	url(r'^list/$', views.list, name='list'),
	url(r'^write/$', views.write, name='write'),
	url(r'^modify/(?P<post_id>\d+)/$', views.modify, name='modify'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

