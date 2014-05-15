from copy import deepcopy
from urlparse import urlparse

from django.views.generic.edit import View
from django.shortcuts import redirect
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
          , submenu_selected = self.__class__.submenu_selected
          , authenticated = request.user.is_authenticated()
          , username = request.user.username
          , styles = self.__class__.styles_list
          , scripts = self.__class__.scripts_list
        ).render(self.doctype, doctype=self.doctype)
    
    def get(self, request):   
        return HttpResponse(self.in_layout(self.body_content, request))

class PageObject(object):
    template = ''
    
    def __init__(self, **context):
        self.template = loader.get_template(self.__class__.template)
        self.context = context
        
    def render(self):
        return Markup( self.template.generate( **self.context ))
    
class SolarisFormViewMixin(object):
    form_outer_template = 'solaris_form_outer.tmpl'
    form_class = None
    form_properties = {
        'css-class' : 'form'
    ,   'post-url'  : '/post'
    ,   'submit'    : 'submit'
    ,   'redirect'  : None
    }
    accept_redirect = False
    form_initial={}
    
    def __init__(self, *args, **kwargs):
        super(SolarisFormViewMixin, self).__init__(*args, **kwargs)
        self.template = loader.get_template(self.__class__.form_outer_template)
        
        self.form_properties = {}
        
        for (prop, default) in self.__class__.form_properties.items():
            self.form_properties[prop] = get_arg(prop,kwargs,default=default)
        
    def render_form(self, form):
        body = Markup( self.template.generate(
            form_items = Markup(form.as_p())
        ,   formclass  = self.form_properties['css-class']
        ,   post_url   = self.form_properties['post-url']
        ,   submit     = self.form_properties['submit']
        )) 
        
        return body
    
    def redirectURL(self, postdata):
        if 'redirect' in postdata and self.__class__.accept_redirect:
            url = urlparse(postdata['redirect'])
            return redirect(url.path)
        elif self.form_properties['redirect']:
            return redirect(self.form_properties['redirect'])
        else:
            return None
        
    def get_form(self, data=None):
        return self.__class__.form_class(data, initial=self.__class__.form_initial)
