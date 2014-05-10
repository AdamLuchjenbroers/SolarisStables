from copy import deepcopy

from django.views.generic.edit import View
from django_genshi import loader
from django.http import HttpResponse
from genshi import Markup

from .utils import get_arg

class SolarisView(View):
    
    styles_list = ['/static/css/solaris.css',]
    scripts_list = ['/static/nicEdit/nicEdit.js',] 
    base_menu = [
          {'title' : 'News', 'url' : '/'},
          {'title' : 'Wiki', 'url' : '/wiki/'},
          {'title' : 'Reference', 'url' : '/reference/'},       
        ]
    menu_selected = None
    submenu = None
    submenu_selected = None

    def __init__(self, *args, **kwargs):         
        master_template = get_arg('master_template', kwargs, 'layout.tmpl')
        self.base_layout = loader.get_template(master_template)
        
        self.doctype = get_arg('doctype', kwargs, 'html')        
        
        self.body_content = get_arg('body', kwargs, Markup('<p>Body Goes Here</p>'))
        
    def get_menu(self, user):
        if user.is_authenticated():
            menu = deepcopy(self.__class__.base_menu)
            
            menu.append( {'title' : 'Stable', 'url' : '/stable'} )
            
            if user.is_staff:            
                menu.append({'title' : 'Admin', 'url' : '/admin'})
                
            return menu
        else:
            return self.__class__.base_menu
                        
        
    
    def in_layout(self, body, request):   
        
        return self.base_layout.generate(
            body=body
          , selected=self.__class__.menu_selected
          , menu=self.get_menu(request.user)
          , submenu = self.__class__.submenu
          , submenu_selected = self.__class__.submenu
          , authenticated = request.user.is_authenticated()
          , username = request.user.username
          , styles = self.__class__.styles_list
          , scripts = self.__class__.scripts_list
        ).render(self.doctype, doctype=self.doctype)
    
    def get(self, request):   
        return HttpResponse(self.in_layout(self.body_content, request))