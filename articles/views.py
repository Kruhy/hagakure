from django.core.paginator import Paginator
from django.http import Http404
from django.shortcuts import redirect, render
from django.views import View

from utils.functions import display_name
from .forms import AddArticleForm, ArticlePublicationStatusForm
from .models import Article, ArticleCategory


class AllArticlesView(View):

    def get(self, request, *args, **kwargs):

        selected_category_name = kwargs['category']

        categories = ArticleCategory.objects.all().order_by('name')

        if request.user.is_staff:
            articles = Article.objects.all().order_by('-created_on')
        elif request.user.is_authenticated:
            articles = Article.objects.filter(is_published=True).all().order_by('-created_on')
        else:
            articles = Article.objects.filter(is_published=True, is_public=True).all().order_by('-created_on')

        if selected_category_name != 'all':
            selected_category = categories.filter(name=selected_category_name).get()
            articles = articles.filter(category=selected_category)
        
        articles_per_page = 9
        paginator = Paginator(articles, articles_per_page)

        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context = {
            'name': display_name(request.user),
            'categories': categories,
            'page_obj': page_obj,
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

        if not request.user.is_staff:
            raise Http404()

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


class AddArticleView(View):

    def get(self, request, *args, **kwargs):

        if not request.user.is_staff:
            raise Http404()
        form = AddArticleForm()
        categories = ArticleCategory.objects.all()
        context = {
            'name': display_name(request.user),
            'categories': categories,
            'form': form,
        }
        return render(request, 'articles/add_article.html', context)

    def post(self, request, *args, **kwargs):
        
        form = AddArticleForm(request.POST)
        article = Article()
        
        if form.is_valid():
            data = form.cleaned_data

            article.title = data['title']
            article.synopsis = data['synopsis']
            article.body = data['body']
            article.is_published = data['is_published']
            article.is_public = data['is_public']
            article.author = request.user
            article.save()
            article.category.set(data['category'])
        
        return redirect('article_list')


class EditArticleView(View):

    def get(self, request, *args, **kwargs):
        if not request.user.is_staff:
            raise Http404()
        
        article_pk = kwargs['pk']
        categories = ArticleCategory.objects.all()
        article = Article.objects.filter(pk=article_pk).get()

        form = AddArticleForm(initial={'title': article.title, 'body': article.body, 'synopsis': article.synopsis,})

        context = {
            'name': display_name(request.user),
            'categories': categories,
            'article': article,
            'form': form,
        }
        return render(request, 'articles/edit_article.html', context)

    def post(self, request, *args, **kwargs):
    
        form = AddArticleForm(request.POST)
        article_pk = kwargs['pk']
        article = Article.objects.filter(pk=article_pk).get()

        if form.is_valid():
            data = form.cleaned_data

            article.title = data['title']
            article.synopsis = data['synopsis']
            article.body = data['body']
            article.is_published = data['is_published']
            article.is_public = data['is_public']
            article.author = request.user
            article.save()
            article.category.set(data['category'])
        
        return redirect('article_list')
