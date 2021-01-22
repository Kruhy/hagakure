from django.http import Http404
from django.shortcuts import redirect, render
from django.views import View

from utils.functions import display_name
from .forms import ArticlePublicationStatusForm
from .models import Article, ArticleCategory


class AllArticlesView(View):

    def get(self, request, *args, **kwargs):

        articles = Article.objects.all().order_by('created_on')
        categories = ArticleCategory.objects.all().order_by('name')

        context = {
            'name': display_name(request.user),
            'articles': articles,
            'categories': categories
        }

        return render(request, 'articles/articles.html', context)


class ArticleView(View):

    def get(self, request, *args, **kwargs):

        article_id = kwargs['pk']
        article = Article.objects.filter(pk=article_id).get()

        if article.is_published or request.user.is_staff:
            if article.is_public or request.user.is_authenticated: 

                context = {
                    'name': display_name(request.user),
                    'article': article,
                }

                return render(request, 'articles/article_details.html', context)

        raise Http404("Article does not exist!")


class ArticlesListView(View):

    def get(self, request, *args, **kwargs):

        articles = Article.objects.all()
        context = {
                'name': display_name(request.user),
                'articles': articles,
            }

        return render(request, 'articles/articles_list.html', context)

    def post(self, request, *args, **kwargs):

        articles = Article.objects.all()
        
        is_published_list =  request.POST.getlist('is_published')
        is_public_list = request.POST.getlist('is_public')

        for article in articles:
            if str(article.pk) in is_published_list:
                article.is_published = True
            else:
                article.is_published = False

            if str(article.pk) in is_public_list:
                article.is_public = True
            else:
                article.is_public = False
            
            article.save()

        return redirect('article_list')
