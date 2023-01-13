from django.urls import path, re_path
from . import views

app_name = "article"
urlpatterns = [
    path('', views.ArticleListView.as_view(), name='articles_list'),
    path('user/<pk>', views.ArticleListView.as_view(), name='user_articles'),
    path('cat/<str:category>', views.ArticleListView.as_view(), name='articles_category_list'),
    re_path('(?P<pk>[-\w]+)/(?P<slug>[-\w]+)', views.ArticleDetailView.as_view(), name='article_detail'),
    path('add-article-comment', views.add_article_comment, name='add_article_comment'),

]
