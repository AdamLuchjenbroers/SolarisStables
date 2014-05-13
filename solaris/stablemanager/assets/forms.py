from solaris.forms import SolarisModelForm

from .models import Pilot

class PilotForm(SolarisModelForm):
    
    class Meta:
        model = Pilot
