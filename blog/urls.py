from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'blog.views.index'),
    url(r'^about/$', 'blog.views.about'),
    url(r'^(?P<year>\d{4})/(?P<month>\w{3})/(?P<day>\d{2})/(?P<slug>[-\w]+)/$',
        'blog.views.post_detail'),
    url(r'^category/(?P<slug>[-\w]+)/$', 'blog.views.category_detail'),
    url(r'^(?P<year>\d{4})/(?P<month>\w{3})/$', 'blog.views.archive_detail'),
    url(r'^comments/(?P<year>\d{4})/(?P<month>\w{3})/(?P<day>\d{2})/(?P<slug>[-\w]+)/$',
        'blog.views.comments'),
)
