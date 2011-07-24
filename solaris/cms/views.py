# -*- coding: iso-8859-1 -*-
from genshi import Markup
from solaris.cms.models import StaticContent, NewsPost
from solaris.core import render_page
from django.shortcuts import get_object_or_404, redirect
from django_genshi import loader


def static_content(request, selected=None):
    # Derive body text
    content = get_object_or_404(StaticContent, url='/%s' % selected).content
    body = Markup(content)
    
    return render_page(body=body, selected=selected, request=request)
    
def news_page(request, selected=None):
    posts = NewsPost.objects.order_by('post_date')[0:5]
    for p in posts:
      p.prepare()
    
    tmpl_news = loader.get_template('news_posts.tmpl')    
    newspage = Markup(tmpl_news.generate(news=posts))
    
    return render_page(body=newspage, selected=selected, request=request)
     
def news_form(request, selected):
    tmpl_news = loader.get_template('news_form.tmpl')    
    newsform = Markup(tmpl_news.generate())
    
    return render_page(body=newsform, selected=None, request=request)

def post_news(request):
    post = NewsPost(
      poster = request.user
    , title = request.POST['title']
    , content = request.POST['content']
    )
    
    post.save()
    
    return redirect('/')
     
def post_news_page(request, selected=None):
    if request.user.has_perm('cms.post_news'):
        if request.method == 'GET':
	    return news_form(request, selected)
	else:
	    return post_news(request)
    else:
        return redirect('/')
     
