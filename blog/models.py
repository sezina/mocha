from django.db import models

# Create your models here.
import datetime
from markdown import markdown
from tagging.fields import TagField

class Category(models.Model):
    title = models.CharField(max_length = 250,
            help_text = "Maximum 250 characters.")
    slug = models.SlugField(unique = True, help_text = "Suggested value \
            automatically generated from title. Must be unique.")
    description = models.TextField(blank = True)

    class Meta:
        ordering = ['title']
        verbose_name_plural = "Categories"

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        pass


class Post(models.Model):
    LIVE_STATUS = 1
    HIDDEN_STATUS = 2
    STATUS_CHOISE = (
        (LIVE_STATUS, 'Live'),
        (HIDDEN_STATUS, 'Hidden'),
    )
    # Core field
    title = models.CharField(max_length = 250,
            help_text = "Maximum 250 characters.")
    body = models.TextField()
    pub_date = models.DateTimeField(default = datetime.datetime.now)
    
    body_html = models.TextField(editable = False, blank = True)

    # metadata
    slug = models.SlugField(unique = True, help_text = "Suggested value \
            automatically generated from title. Must be unique.")
    commentable = models.BooleanField(default = True)
    status = models.IntegerField(choice = STATUS_CHOISE, default = LIVE_STATUS,
            help_text = "Only post with live status will be publicly displayed.")

    categories = models.ManyToManyField(Category)
    tags = TagField(help_text = "Seperate tags with space.")

    class Meta:
        ordering = ['-pub_date']

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        pass
