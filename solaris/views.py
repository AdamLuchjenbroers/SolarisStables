from copy import deepcopy
from urlparse import urlparse

from django.views.generic.edit import View
from django.shortcuts import redirect, render_to_response
from django_genshi import loader as genshi_loader
from django.template import Context, RequestContext

from genshi import Markup

from .utils import get_arg

class SolarisViewMixin(object):
    styles_list = ['/static/css/solaris.css',]
    scripts_list = ['/static/nicEdit/nicEdit.js',] 
    base_menu = [
          {'title' : 'News', 'url' : '/', 'visible' : 'always'},
          {'title' : 'Wiki', 'url' : '/wiki/', 'visible' : 'always'},
          {'title' : 'Reference', 'url' : '/reference/', 'visible' : 'always'},       
          {'title' : 'Stable', 'url' : '/stable/', 'visible' : 'login'},       
          {'title' : 'Admin', 'url' : '/admin', 'visible' : 'admin'},       
        ]
    menu_selected = None
    submenu = None
    submenu_selected = None

    def __init__(self, *args, **kwargs):
        self.template_name = get_arg('master_template', kwargs, 'solaris_layout.tmpl')
        
        self.doctype = get_arg('doctype', kwargs, 'html')        
        
        self.body_content = get_arg('body', kwargs, Markup('<p>Body Goes Here</p>'))
        
    def get_menu(self):
            return self.__class__.base_menu      
        
    def get_context_data(self, **kwargs):
        try:
            page_context = super(SolarisViewMixin, self).get_context_data(**kwargs)
        except AttributeError:
            page_context = Context()
        
        page_context['selected'] = self.__class__.menu_selected
        page_context['menu'] = self.get_menu()
        page_context['submenu'] = self.__class__.submenu
        page_context['submenu_selected'] = self.__class__.submenu_selected
        page_context['styles'] = self.__class__.styles_list
        page_context['scripts'] = self.__class__.scripts_list
        
        if not 'body' in page_context:
             page_context['body'] = '<p>Body Goes Here</p>'
        
        return page_context

class SolarisView(SolarisViewMixin, View):
    
    def in_layout(self, body, request):
        page_context = self.get_context_data(request=request)
        page_context['body'] = body
        page_context['visibility'] = ['always']
                
        return render_to_response(self.template_name, page_context, RequestContext(request) )

    def get(self, request):   
        return self.in_layout(self.body_content, request)

class PageObject(object):
    template = ''
    
    def __init__(self, **context):
        self.template = genshi_loader.get_template(self.__class__.template)
        self.context = context
        
    def render(self):
        return Markup( self.template.generate( **self.context ))
    
class SolarisFormViewMixin(object):
    form_outer_template = 'solaris_form_outer.genshi'
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
        self.template = genshi_loader.get_template(self.__class__.form_outer_template)
        
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
