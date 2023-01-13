from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from django.views.generic import DetailView
from django.views.generic.list import ListView
from article_module.models import Article, ArticleCategory, ArticleComment
from jalali_date import datetime2jalali, date2jalali


class ArticleListView(ListView):
    template_name = 'article_module/articles_page.html'
    model = Article
    context_object_name = 'articles'
    ordering = ['-created']
    paginate_by = 6

    def get_queryset(self):
        query = super(ArticleListView, self).get_queryset()
        category_name = self.kwargs.get('category')
        user_id = self.kwargs.get('pk')
        if category_name is not None:
            query = query.filter(selected_categories__url_title__iexact=category_name)
        elif user_id is not None:
            query = query.filter(author__pk__iexact=user_id)
        data = query.filter(is_active=True)
        return data


class ArticleDetailView(DetailView):
    template_name = 'article_module/article_detail_page.html'
    model = Article

    def get_queryset(self):
        query = super(ArticleDetailView, self).get_queryset()
        slug = self.kwargs.get('slug')
        if slug is not None:
            query = query.filter(slug__iexact=slug)
        data = query.filter(is_active=True)
        return data

    def get_context_data(self, **kwargs):
        context = super(ArticleDetailView, self).get_context_data()
        article: Article = kwargs.get('object')
        context['comment'] = ArticleComment.objects.filter(article_id=article.id, parent=None).order_by(
            '-created').prefetch_related(
            'articlecomment_set')
        context['comment_count'] = ArticleComment.objects.filter(article_id=article.id).count()
        return context


def add_article_comment(request):
    if request.user.is_authenticated:
        article_comment = request.GET.get('article_comment')
        article_id = request.GET.get('article_id')
        parent_id = request.GET.get('parent_id')
        print(article_comment, article_id, parent_id)
        new_comment = ArticleComment(article_id=article_id, text=article_comment, user_id=request.user.id,
                                     parent_id=parent_id)
        new_comment.save()
        context = {
            'comment': ArticleComment.objects.filter(article_id=article_id, parent=None).order_by(
                '-created').prefetch_related(
                'articlecomment_set'),
            'comment_count': ArticleComment.objects.filter(article_id=article_id).count()
        }
        return render(request, 'article_module/includes/article_comment_partial.html', context)
    return HttpResponse('hello')


def article_categories_component(request):
    article_main_categories = ArticleCategory.objects.prefetch_related('articlecategory_set').filter(is_active=True,
                                                                                                     parent_id=None)
    context = {
        'main_categories': article_main_categories
    }
    return render(request, 'article_module/components/article_categories_component.html', context)
