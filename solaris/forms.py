
from django.forms import ModelForm
from django.utils.html import conditional_escape
from django.utils.encoding import force_unicode

class SolarisModelForm(ModelForm):
    
    def __init__(self, *args, **kwargs):
        super(SolarisModelForm, self).__init__(*args, **kwargs)
        if 'field_format' in kwargs:
            self.field_format = kwargs['field_format']
        else:
            self.field_format = '<p id="{label}"><label for="id_{label}">{label}:</label> {field} {errors}</p>'
            
        if 'error_format' in kwargs:
            self.error_format = kwargs['error_format']
        else:
            self.error_format = '<span class="fielderror">{error}</span>'

    def renderErrors(self, fieldName):
        outputHTML = ''
        
        if fieldName in self.errors:
            for fieldError in self.errors[fieldName]:
                print 'E: %s' % conditional_escape(force_unicode(fieldError))  
                outputHTML += self.error_format.format(error=conditional_escape(force_unicode(fieldError)))
        
        return outputHTML
                      
    def renderField(self, fieldName):
        
        fieldObj  = self[fieldName]
        fieldLabel = fieldObj.label
                
        if fieldLabel is None:
            fieldLabel = fieldName
            
        fieldLabel = conditional_escape(force_unicode(fieldLabel))
                
        if fieldName in self.errors:
            fieldError = self.renderErrors(fieldName)
        else:
            fieldError = ''
            
        return self.field_format.format(label=fieldLabel, field=fieldObj, errors=fieldError)
    
    def as_p(self):
        pageHTML = ''
        
        if '__all__' in self.errors:
            pageHTML += '<span class=form_error><p>Unable to process form</p>%s</span>' % self.errors['__all__']
            
        for fieldName in self.fields.keys():
            pageHTML += self.renderField(fieldName)
            
        #pageHTML += ModelForm.as_p(self)
        # if self.errors
        # errorHeader =
        return pageHTML

            
        
             
        