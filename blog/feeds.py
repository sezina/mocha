from django.core.exceptions import ObjectDoesNotExist
from django.utils.feedgenerator import Atom1Feed
from django.contrib.sites.models import Site
from django.contrib.syndication.views import Feed
from models import Post

current_site = Site.objects.get_current()

class LatestPostsFeed(Feed):
    description = "Latest posts posted to %s" % current_site.name
    feed_type = Atom1Feed
    link = "/feeds/"
    title = "%s: Latest posts" % current_site.name

    def items(self):
        return Post.live.all()[:10]

    def item_title(self, item):
        return item.title

    def item_pubdate(self, item):
        return item.pub_date

    def item_guid(self, item):
        return "tag:%s,%s:%s" % (current_site.domain,
                item.pub_date.strftime('%Y-%m-%d'),
                item.get_absolute_url())

    def item_categories(self, item):
        return [category.title for category in item.categories.all()]
