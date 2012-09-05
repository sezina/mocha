from django.contrib import admin

from models import *


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = { 'slug': ['title'] }

admin.site.register(Category, CategoryAdmin)


class PostAdmin(admin.ModelAdmin):
    prepopulated_fields = { 'slug': ['title'] }

admin.site.register(Post, PostAdmin)


admin.site.register(Link)

class CommentAdmin(admin.ModelAdmin):
    display_fields = ["post", "visitor", "comment_date"]

admin.site.register(Comment, CommentAdmin)
