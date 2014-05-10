# -*- coding: iso-8859-1 -*-
from genshi import Markup
from django.shortcuts import redirect
from django_genshi import loader
from django.contrib.auth.decorators import permission_required
from django.http import HttpResponse

from solaris.views import SolarisView
from solaris.cms.models import NewsPost

class NewsView(SolarisView):
    menu_selected = 'News'
    
class NewsListView(NewsView):
    def get(self, request):
        posts = NewsPost.objects.order_by('post_date').reverse()[0:5]
        for p in posts:
            p.prepare()
        
        tmpl_news = loader.get_template('cms/news_posts.tmpl')    
        newspage = Markup(tmpl_news.generate(news=posts, adminbar=request.user.has_perm('cms.post_news')))
        
        return HttpResponse(self.in_layout(newspage, request))
    
class NewsPostFormView(NewsView):

    @permission_required('cms.post_news')    
    def dispatch(self, *args, **kwargs):
        super(NewsPostFormView, self).dispatch(*args, **kwargs)
        
    def get(self, request):
        tmpl_news = loader.get_template('cms/news_form.tmpl')    
        newsform = Markup(tmpl_news.generate())
    
        return HttpResponse(self.in_layout(newsform, request))
    
    def post(self, request):
        if ((len(request.POST['title']) > 0) and (len(request.POST['content']) > 0)):
            post = NewsPost(poster = request.user, title = request.POST['title'], content = request.POST['content'])    
            post.save()
            return redirect('/')
        else:
            return self.get(request)
