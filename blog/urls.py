from django.conf.urls import patterns, include, url
from feeds import LatestPostsFeed

urlpatterns = patterns('blog.views',
    url(r'^$', 'index'),
    url(r'^about/$', 'about'),
    url(r'^(?P<year>\d{4})/(?P<month>\w{3})/(?P<day>\d{2})/(?P<slug>[-\w]+)/$',
        'post_detail'),
    url(r'^category/(?P<slug>[-\w]+)/$', 'category_detail'),
    url(r'^(?P<year>\d{4})/(?P<month>\w{3})/$', 'archive_detail'),
    url(r'^add_comment/(?P<pk>\d+)/$', 'add_comment'),
)

urlpatterns += patterns('',
    url(r'^feeds/$', LatestPostsFeed()),
)
