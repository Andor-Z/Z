from django.contrib import admin

# Register your models here.
from .models import Article, Category, Tag, BlogComment


admin.site.register(Article)
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(BlogComment)