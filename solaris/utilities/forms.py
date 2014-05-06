'''
   ModelForm for validating Mech Data input loaded from SSW files
   This form is not intended to be rendered to a page
'''

from django.forms import ModelForm
from django.forms.models import model_to_dict

from solaris.warbook.mech.models import MechDesign
from solaris.utilities.parser import SSWFile

class MechValidationForm(ModelForm):
    def __init__(self, *args, **kwargs):
        if isinstance(args[0],dict):
            args[0]['mech_key'] = '%s|%s' % (args[0]['mech_name'].lower(), args[0]['mech_code'].lower())
        
        super(MechValidationForm,self).__init__(*args, **kwargs)
        
    class Meta:
        model = MechDesign
        
    @staticmethod
    def load_from_xml(xmlfilename, xmlrelativename):
        sswData = SSWFile(xmlfilename)
        
        try:
            mech_object = MechDesign.objects.get(ssw_filename=xmlrelativename)
            mech_dict = model_to_dict(mech_object)
        except MechDesign.DoesNotExist:
            mech_object = MechDesign()
            mech_dict = {}
            mech_dict['ssw_filename'] = xmlrelativename
        
            
        mech_dict['mech_name'] = sswData.get_name()
        mech_dict['mech_code'] = sswData.get_code()
        mech_dict['credit_value'] = sswData.get_cost()
        mech_dict['bv_value'] = sswData.get_bv()
        mech_dict['tonnage'] = sswData.get_tonnage()
        mech_dict['engine_rating'] = sswData.get_enginerating()
        mech_dict['is_omni'] = sswData.is_omni()
        
        return MechValidationForm(mech_dict, instance=mech_object)
        