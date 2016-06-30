from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^article/(?P<article_id>\d+)/$', views.ArticleDetailView.as_view(), name='detail'),   # 正则中\d表示[0-9]
    url(r'^article/(?P<article_id>\d+)/comment/$', views.CommentPostView.as_view(), name='comment'),
    url(r'^category/(?P<cate_id>\d+)/$', views.CategoryView.as_view(), name='category'),
    url(r'^tag/(?P<tag_id>\d+)/$', views.TagView.as_view(), name='tag'),
    url(r'^archive/(?P<year>\d{4})/(?P<month>\d{1,2})/$', views.ArchiveView.as_view(), name='archive'),
]
