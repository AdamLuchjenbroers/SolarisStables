import re

from django.views.generic.edit import View
from django_genshi import loader
from .utils import get_arg
from solaris.cms.models import StaticContent
from django.http import HttpResponse
from genshi import Markup

class SolarisView(View):
    
    def get_styles(self):
        return [
            '/static/css/solaris.css'
        ]
    
    def get_scripts(self):
        return [
            '/static/nicEdit/nicEdit.js'
        ]
        
    def __init__(self, *args, **kwargs):         
        master_template = get_arg('master_template', kwargs, 'layout.tmpl')
        self.base_layout = loader.get_template(master_template)
        
        self.doctype = get_arg('doctype', kwargs, 'html')        
        
        self.body_content = get_arg('body', kwargs, Markup('<p>Body Goes Here</p>'))
        
    def get_menu(self):
        return StaticContent.objects.filter(toplevel=True).order_by('order')
    
    def get_submenu(self):
        return None
    
    def in_layout(self, body, request):
        
        url_firstterm = re.compile('^(/[^/]*).*$')
        url_match = url_firstterm.match(request.get_full_path())
        if url_match:
            selected = url_match.group(1)
        else:
            selected = None            
        
        return self.base_layout.generate(
            body=body
          , selected=selected
          , menu=self.get_menu()
          , sub_selected=None
          , submenu = self.get_submenu()
          , authenticated = request.user.is_authenticated()
          , username = request.user.username
          , styles = self.get_styles()
          , scripts = self.get_scripts()
        ).render(self.doctype, doctype=self.doctype)
    
    def get(self, request):   
        return HttpResponse(self.in_layout(self.body_content, request))