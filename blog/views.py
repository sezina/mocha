# Create your views here.
from datetime import datetime
from django.shortcuts import render_to_response, get_object_or_404
from django.views.generic.list_detail import object_list
from django.template import RequestContext
from django.http import HttpResponseRedirect
from models import *


def archive_list():
    this_year = datetime.datetime.now().year
    posts = Post.live.order_by('pub_date')
    if posts.count() == 0:
        return []
    oldest_year = posts[0].pub_date.year

    archive_time_list = {}
    for post in posts:
        archive_time_list["%s/%s/" % (post.pub_date.strftime("%Y"),
                          post.pub_date.strftime("%b").lower())] = 0

    return [item for item in archive_time_list]


def index(request):
    time_line = archive_list()
    return render_to_response('blog/index.html',
            {'posts': Post.live.all(),
             'categories': Category.objects.all(),
             'links': Link.objects.all(),
             'time_line': time_line})


def about(request):
    time_line = archive_list()
    return render_to_response('about.html',
            {'posts': Post.live.all(),
             'categories': Category.objects.all(),
             'links': Link.objects.all(),
             'time_line': time_line})


def post_detail(request, year, month, day, slug):
    time_line = archive_list()
    import datetime
    import time
    date_stamp = time.strptime(year + month + day, "%Y%b%d")
    pub_date = datetime.date(*date_stamp[:3])
    post = get_object_or_404(Post, pub_date__year=pub_date.year,
                                   pub_date__month=pub_date.month,
                                   pub_date__day=pub_date.day,
                                   slug=slug)
    return render_to_response('blog/post_detail.html',
            {'post': post,
             'time_line': time_line,
             'categories': Category.objects.all(),
             'links': Link.objects.all(),
             'comments': post.comment_set.all()},
            context_instance=RequestContext(request))


def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    time_line = archive_list()
    return render_to_response('blog/category_detail.html',
            {'posts': category.post_set.all(),
             'category': category,
             'categories': Category.objects.all(),
             'links': Link.objects.all(),
             'time_line': time_line})


def archive_detail(request, year, month):
    time_line = archive_list()
    import datetime
    import time
    date_stamp = time.strptime(year + month + "1", "%Y%b%d")
    pub_date = datetime.date(*date_stamp[:3])
    posts = Post.live.filter(pub_date__year=pub_date.year,
            pub_date__month=pub_date.month)
    return render_to_response('blog/archive_detail.html',
            {'posts': posts,
             'categories': Category.objects.all(),
             'links': Link.objects.all(),
             'time_line': time_line})


def add_comment(request, pk):
    post = Post.live.get(pk=int(pk))
    if request.POST:
        visitor = request.POST.get('visitor', None)
        email = request.POST.get('email', None)
        body = request.POST.get('body', None)

        if visitor and email and body:
            comment = Comment()
            comment.visitor = visitor
            comment.email = email
            comment.body = body
            comment.comment_date = datetime.datetime.now()
            comment.post = post
            comment.save()
    return HttpResponseRedirect(post.get_absolute_url())
