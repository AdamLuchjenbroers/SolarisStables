
from django.forms import ModelForm, Form
from django.utils.html import conditional_escape
from django.utils.encoding import force_unicode
from django_genshi import loader
from genshi import Markup
from .utils import get_arg

def escape_unicode(string):
    return conditional_escape(force_unicode(string))

class SolarisFormMixin(object):
    
    inner_form_template = 'solaris_form.tmpl'
        
    def __init__(self, *args, **kwargs):
        self.template = loader.get_template(self.__class__.inner_form_template)
        
        self.redirectURL = get_arg('redirect', kwargs)
        super(SolarisFormMixin, self).__init__(*args, **kwargs)

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
    
    def getAllFields(self):
        fieldSet = []   
        for fieldName in self.fields.keys():
            fieldSet.append(self.getField(fieldName))
        
        return fieldSet
    
    def as_p(self):
        
        if '__all__' in self.errors:
            formErrors = self.errors['__all__']
        else:
            formErrors = None
        
        return self.template.generate(formErrors=formErrors, form=self.getAllFields(), redirect=self.redirectURL)

class SolarisFixedFormMixin(SolarisFormMixin):
    """ 
    Variant of SolarisFormMixin that passes the list of fields to the template as a dictionary, so that the field placement
    can be more tightly controlled / customized
    """
    inner_form_template = None #This mixin expects a bespoke template for each form, so just fail if this hasn't been set
    
    def getAllFields(self):        
        fieldSet = dict()    
        for fieldName in self.fields.keys():
            fieldSet[fieldName] = self.getField(fieldName)
        
        return fieldSet

class SolarisModelForm(SolarisFormMixin, ModelForm):
    pass

class SolarisForm(SolarisFormMixin, Form):
    pass

class SolarisInlineForm(SolarisFormMixin, ModelForm):
    inner_form_template = 'solaris_form_inline.tmpl'
    
    def as_p(self):
        return Markup( super(SolarisInlineForm, self).as_p())
           
        
             
        