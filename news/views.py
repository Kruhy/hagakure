from django.http import Http404
from django.shortcuts import redirect, render
from django.views import View


from utils.functions import display_name
from .models import News


class AllNewsView(View):

    def get(self, request, *args, **kwargs):

        if request.user.is_staff:
            news = News.objects.all().order_by('-created_on')
        elif request.user.is_authenticated:
            news = News.objects.filter(is_published=True).all().order_by('-created_on')
        else:
            news = News.objects.filter(is_published=True, is_public=True).all().order_by('-created_on')
        
        creation_years = News.objects.dates('created_on','year', 'DESC')
        creation_months = News.objects.dates('created_on','month', 'DESC')
        
        context = {
            'name': display_name(request.user),
            'all_news': news,
            'creation_years': creation_years,
            'creation_months': creation_months,
        }
        return render(request, 'news/news.html', context)


class NewsListView(View):

    def get(self, request, *args, **kwargs):
        
        if not request.user.is_staff:
            raise Http404()

        news = News.objects.all().order_by('-created_on')
        context = {
            'name': display_name(request.user),
            'all_news': news
        }
        return render(request, 'news/news_list.html', context)

    def post(self, request, *args, **kwargs):

        all_news = News.objects.all()
        
        is_published_list =  request.POST.getlist('is_published')
        is_public_list = request.POST.getlist('is_public')
        
        for news in all_news:
            if str(news.pk) in is_published_list:
                news.is_published = True
            else:
                news.is_published = False

            if str(news.pk) in is_public_list:
                news.is_public = True
            else:
                news.is_public = False
            exp_date = request.POST['exp_date?{}'.format(news.pk)]

            if exp_date=='':
                exp_date=None
                
            news.expiration_date = exp_date
            news.save()

        return redirect('news_list')    
