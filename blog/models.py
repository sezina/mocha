from django.db import models
from django.forms import ModelForm
from django.utils.encoding import smart_str

# Create your models here.
import datetime
from markdown import markdown
from tagging.fields import TagField


class Category(models.Model):
    title = models.CharField(max_length=250,
            help_text="Maximum 250 characters.")
    slug = models.SlugField(unique=True, help_text="Suggested value \
            automatically generated from title. Must be unique.")
    description = models.TextField(blank=True)

    class Meta:
        ordering = ['title']
        verbose_name_plural = "Categories"

    def __unicode__(self):
        return self.title

    def live_post_set(self):
        return self.post_set.filter(status=Post.LIVE_STATUS)

    def get_absolute_url(self):
        return "/category/%s/" % self.slug


class LiveEntryManager(models.Manager):
    def get_query_set(self):
        return super(LiveEntryManager, self).get_query_set().filter(status=
                self.model.LIVE_STATUS)


class Post(models.Model):
    LIVE_STATUS = 1
    HIDDEN_STATUS = 2
    STATUS_CHOISE = (
        (LIVE_STATUS, 'Live'),
        (HIDDEN_STATUS, 'Hidden'),
    )
    # Core field
    title = models.CharField(max_length=250,
            help_text="Maximum 250 characters.")
    body = models.TextField()
    pub_date = models.DateTimeField(default=datetime.datetime.now)

    body_html = models.TextField(editable=False, blank=True)

    # metadata
    slug = models.SlugField(unique=True, help_text="Suggested value \
            automatically generated from title. Must be unique.")
    commentable = models.BooleanField(default=True)
    status = models.IntegerField(choices=STATUS_CHOISE, default=LIVE_STATUS,
            help_text="Only post with live status will be publicly displayed.")

    categories = models.ManyToManyField(Category)
    tags = TagField(help_text="Seperate tags with space.")

    live = LiveEntryManager()

    class Meta:
        ordering = ['-pub_date']

    def __unicode__(self):
        return self.title

    def save(self, force_insert=False, force_update=False):
        self.body_html = markdown(self.body, ['codehilite'])
        filename = "public/static_html/%s_%s_%s_%s.html" % (
                                        self.pub_date.strftime("%Y"),
                                        self.pub_date.strftime("%b").lower(),
                                        self.pub_date.strftime("%d"),
                                        self.slug)
        f = file(filename, "wb")
        f.write(smart_str(self.body_html))
        f.close()
        super(Post, self).save(force_insert, force_update)

    def get_absolute_url(self):
        return "/%s/%s/%s/%s/" % (self.pub_date.strftime("%Y"),
                                  self.pub_date.strftime("%b").lower(),
                                  self.pub_date.strftime("%d"),
                                  self.slug)


class Link(models.Model):
    title = models.CharField(max_length=250)
    url = models.URLField('URL', unique=True)
    logo_url = models.CharField(max_length=250)

    class Meta:
        ordering = ['title']

    def __unicode__(self):
        return self.title


class Comment(models.Model):
    visitor = models.CharField(max_length=60)
    email = models.EmailField()
    body = models.TextField()
    comment_date = models.DateTimeField(default=datetime.datetime.now)
    post = models.ForeignKey(Post)

    # metadata
    body_html = models.TextField(editable=False)

    class Meta:
        ordering = ['-comment_date']

    def __unicode__(self):
        return "%s comments at %s" % (self.visitor,
                self.comment_date.strftime("%Y%b%d"))

    def save(self, force_insert=False, force_update=False):
        self.body_html = markdown(self.body, ['codehilite'])
        super(Comment, self).save(force_insert, force_update)
