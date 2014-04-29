
from django.views.generic.edit import View
from django_genshi import loader
from .utils import get_arg
from solaris.cms.models import StaticContent
from django.http import HttpResponse
from genshi import Markup

class SolarisView(View):
    
    def __init__(self, *args, **kwargs): 
        self.navigation_options = StaticContent.objects.filter(toplevel=True).order_by('order')
        
        master_template = get_arg('master_template', kwargs, 'layout.tmpl')
        self.template = loader.get_template(master_template)
        
        self.doctype = get_arg('doctype', kwargs, 'html')        
        self.selected = '/%s' % get_arg('selected', kwargs, '')
        
        self.body_content = get_arg('body', kwargs, Markup('<p>Body Goes Here</p>'))
    
    def body(self):
        return self.body_content
    
    def get(self, request):
        output = self.template.generate(
            body=self.body()
          , selected=self.selected
          , menu=self.navigation_options
          , authenticated = request.user.is_authenticated()
          , username = request.user.username
        ).render(self.doctype, doctype=self.doctype)
        
        return HttpResponse(output)