from solaris.forms import SolarisModelForm

from .models import Pilot

class PilotForm(SolarisModelForm):
    

    class Meta:
        model = Pilot
        fields = ('pilot_name', 'pilot_callsign', 'pilot_rank', 'skill_gunnery', 'skill_pilotting', 'exp_character_points')