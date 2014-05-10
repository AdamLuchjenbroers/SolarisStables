import re

from django.views.generic.edit import View
from django_genshi import loader
from .utils import get_arg
from solaris.cms.models import StaticContent
from django.http import HttpResponse
from genshi import Markup

class SolarisView(View):
    
    styles_list = ['/static/css/solaris.css',]
    scripts_list = ['/static/nicEdit/nicEdit.js',] 
    menu = None
    menu_selected = None
    submenu = None
    submenu_selected = None

    def __init__(self, *args, **kwargs):         
        master_template = get_arg('master_template', kwargs, 'layout.tmpl')
        self.base_layout = loader.get_template(master_template)
        
        self.doctype = get_arg('doctype', kwargs, 'html')        
        
        self.body_content = get_arg('body', kwargs, Markup('<p>Body Goes Here</p>'))
        
    def get_menu(self):
        return StaticContent.objects.filter(toplevel=True).order_by('order')
    
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
          , submenu = self.__class__.submenu
          , submenu_selected = self.__class__.submenu
          , authenticated = request.user.is_authenticated()
          , username = request.user.username
          , styles = self.__class__.styles_list
          , scripts = self.__class__.scripts_list
        ).render(self.doctype, doctype=self.doctype)
    
    def get(self, request):   
        return HttpResponse(self.in_layout(self.body_content, request))