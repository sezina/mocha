from django.contrib import admin
from models import *


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ['title']}

admin.site.register(Category, CategoryAdmin)


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'pub_date', 'slug', 'status')
    date_hierarchy = 'pub_date'
    prepopulated_fields = {'slug': ['title']}

admin.site.register(Post, PostAdmin)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('visitor', 'post', 'comment_date')

admin.site.register(Comment, CommentAdmin)


class LinkAdmin(admin.ModelAdmin):
    list_display = ('title', 'url', 'logo_url')

admin.site.register(Link, LinkAdmin)
