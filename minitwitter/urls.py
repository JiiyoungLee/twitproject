from django.conf.urls import url, include
from django.contrib.auth import views as auth_views
from minitwitter import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^auth/', include('django.contrib.auth.urls')),
	url(r'^signin/$', views.SigninView.as_view(), name='signin'),
	url(r'^timeline/$', views.TimelineView.as_view(), name='timeline'),
	url(r'^timeline/me$', views.MyTimelineView.as_view(), name='my_timeline'),
	url(r'^articles/write$', views.WriteArticleView.as_view(), name='write_article'),
	url(r'^articles/modify/(?P<article_id>\d+)/$', views.ModifyArticleView.as_view(), name='modify_article'),
	url(r'^uploads/(?P<file>.+)', views.uploads, name='upload'),
	url(r'^modify/me', views.ModifyUserView.as_view(), name='modify_user'),
	url(r'^delete/image/(?P<photo_id>\d+)', views.delete_image, name='delete_image'),
	url(r'^auth/check/username/(?P<user_name>.+)', views.check_user_name, name='check_username'),
	url(r'^auth/check/nickname/(?P<nickname>.+)', views.check_nickname, name='check_nickname'),
	url(r'^articles/search/(?P<hashtag>.+)', views.SearchArticleView.as_view(), name='search_article'),
	url(r'^timeline/public$', views.ArticleList.as_view(), name='public_timeline'),
	url(r'^articles/public/search/(?P<hashtag>.+)$', views.SearchArticleList.as_view(), name='public_search_article'),
	url(r'^comments/(?P<article_id>\d+)/$', views.AddComment.as_view(), name='comment'),
	url(r'^comments/modify/(?P<comment_id>\d+)$', views.ModifyComment.as_view(), name='modify_comment'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

