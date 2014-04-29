
from django.views.generic.edit import View
from django_genshi import loader
from .utils import get_arg
from solaris.cms.models import StaticContent
from django.http import HttpResponse
from genshi import Markup

class SolarisView(View):
    
    def __init__(self, *args, **kwargs):         
        master_template = get_arg('master_template', kwargs, 'layout.tmpl')
        self.base_layout = loader.get_template(master_template)
        
        self.doctype = get_arg('doctype', kwargs, 'html')        
        self.selected = '/%s' % get_arg('selected', kwargs, '')
        
        self.body_content = get_arg('body', kwargs, Markup('<p>Body Goes Here</p>'))
        
    def get_menu(self):
        return StaticContent.objects.filter(toplevel=True).order_by('order')
    
    def in_layout(self, body, request):
        return self.base_layout.generate(
            body=body
          , selected=self.selected
          , menu=self.get_menu()
          , authenticated = request.user.is_authenticated()
          , username = request.user.username
        ).render(self.doctype, doctype=self.doctype)
    
    def get(self, request):   
        return HttpResponse(self.in_layout(self.body_content, request))