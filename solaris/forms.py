
from django.forms import ModelForm, Form
from django.utils.html import conditional_escape
from django.utils.encoding import force_unicode
from django_genshi import loader
from genshi import Markup
from .utils import get_arg

def escape_unicode(string):
    return conditional_escape(force_unicode(string))

class SolarisFormMixin():    
    def __init__(self, *args, **kwargs):
        templateName = get_arg('template', kwargs, default='solaris_form.tmpl')
        self.template = loader.get_template(templateName)
        
        self.redirectURL = get_arg('redirect', kwargs)

    def getErrors(self, fieldName):
        errorList=[]
        
        if fieldName in self.errors:
            for fieldError in self.errors[fieldName]:
                errorList.append(escape_unicode(fieldError))
        else:
            return None
        
        return errorList

    def getField(self, fieldName):
        fieldData={}
        
        fieldData['object'] = self[fieldName]
        fieldData['markup'] = Markup(fieldData['object'])
        
        if fieldData['object'].label is None:
            fieldData['label'] = escape_unicode(fieldName)
        else:
            fieldData['label'] = escape_unicode(fieldData['object'].label)
            
        fieldData['errors'] = self.getErrors(fieldName)
        fieldData['info'] = None
        
        if fieldData['errors']:
            fieldData['state'] = 'error'
        elif fieldData['info']:
            fieldData['state'] = 'info'
        else:
            fieldData['state'] = 'basic'
        
        return fieldData
    
    def as_p(self):
        
        if '__all__' in self.errors:
            formErrors = self.errors['__all__']
        else:
            formErrors = None
            
        fieldSet = []    
        for fieldName in self.fields.keys():
            fieldSet.append(self.getField(fieldName))
        
        return self.template.generate(formErrors=formErrors, form=fieldSet, redirect=self.redirectURL)


class SolarisModelForm(SolarisFormMixin, ModelForm):

    def __init__(self, *args, **kwargs):
        SolarisFormMixin.__init__(self, *args, **kwargs)
        ModelForm.__init__(self,*args, **kwargs)

class SolarisForm(SolarisFormMixin, Form):

    def __init__(self, *args, **kwargs):
        SolarisFormMixin.__init__(self, *args, **kwargs)
        Form.__init__(self,*args, **kwargs)
           
        
             
        