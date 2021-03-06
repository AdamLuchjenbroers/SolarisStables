from django.views.generic import TemplateView, FormView

from solaris.views import SolarisViewMixin
from solaris.cms.models import NewsPost
from solaris.cms.forms import NewsPostForm
    
class NewsListView(SolarisViewMixin, TemplateView):
    menu_selected = 'News'
    template_name = 'cms/news.tmpl'

    def get_context_data(self, **kwargs):
        page_context = super(NewsListView, self).get_context_data(**kwargs)
        
        page_context['news'] = NewsPost.objects.order_by('post_date').reverse()[0:5]
        page_context['body'] = '<p>Template Broken</p>'
        return page_context

class NewsPostFormView(SolarisViewMixin, FormView):
    menu_selected = 'News'
    template_name = 'cms/newspost.tmpl'
    form_class = NewsPostForm
    success_url = '/'
    
    def form_valid(self, form):
        new_post = form.instance
        new_post.poster = self.request.user
        new_post.save()
        
        return super(NewsPostFormView, self).form_valid(form)       
