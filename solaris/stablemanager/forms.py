from solaris.forms import SolarisModelForm
from .models import Stable

class StableRegistrationForm(SolarisModelForm):
    
    class Meta:
        model = Stable
    