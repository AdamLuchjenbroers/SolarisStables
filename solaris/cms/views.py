# -*- coding: iso-8859-1 -*-
from genshi import Markup
from solaris.cms.models import StaticContent, NewsPost
from solaris.core import render_page
from django.shortcuts import get_object_or_404
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
        
