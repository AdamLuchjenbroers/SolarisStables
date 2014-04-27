
from django.forms import ModelForm
from django.utils.html import conditional_escape
from django.utils.encoding import force_unicode
from django_genshi import loader
from genshi import Markup

def escape_unicode(string):
    return conditional_escape(force_unicode(string))

class SolarisFormMixin():    
    def __init__(self, *args, **kwargs):
        if 'template' in kwargs:
            self.template = loader.get_template(kwargs['template'])
        else:
            self.template = loader.get_template('solaris_form.tmpl')

        
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
        return fieldData
    
    def as_p(self):
        
        if '__all__' in self.errors:
            formErrors = self.errors['__all__']
        else:
            formErrors = None
            
        fieldSet = []    
        for fieldName in self.fields.keys():
            fieldSet.append(self.getField(fieldName))
        
        return self.template.generate(formErrors=formErrors, form=fieldSet)


class SolarisModelForm(SolarisFormMixin, ModelForm):

    def __init__(self, *args, **kwargs):
        SolarisFormMixin.__init__(self, *args, **kwargs)
        ModelForm.__init__(self,*args, **kwargs)

            
        
             
        