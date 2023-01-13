from django.contrib import admin
from . import models
from .models import Article


class ArticleCategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'parent', 'is_active']
    list_filter = ['title', 'parent', 'url_title', 'is_active']


class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'is_active', 'created']
    list_filter = ['title', 'author', 'selected_categories', 'created', 'is_active']

    def save_model(self, request, obj: Article, form, change):
        if not change:
            obj.author = request.user
        return super().save_model(request, obj, form, change)


class ArticleCommentAdmin(admin.ModelAdmin):
    list_display = ['article','user', 'parent']
    list_filter = ['article', 'user']


admin.site.register(models.ArticleCategory, ArticleCategoryAdmin)
admin.site.register(models.Article, ArticleAdmin)
admin.site.register(models.ArticleComment, ArticleCommentAdmin)
