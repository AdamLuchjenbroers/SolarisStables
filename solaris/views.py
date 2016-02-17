from django.template import Context

class SolarisViewMixin(object):
    menu_selected = None
    submenu = None
    submenu_selected = None     
    login_url = '/login'
        
    def get_context_data(self, **kwargs):
        try:
            page_context = super(SolarisViewMixin, self).get_context_data(**kwargs)
        except AttributeError:
            page_context = Context()
        
        page_context['selected'] = self.__class__.menu_selected
        
        if not 'body' in page_context:
            page_context['body'] = '<p>Body Goes Here</p>'
        
        return page_context
