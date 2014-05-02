from django_genshi import loader
from genshi import Markup
from django.shortcuts import get_object_or_404
from django.http import HttpResponse

from solaris.warbook.views import ReferenceView
from solaris.warbook.pilotskill import models

class DisciplineListView(ReferenceView):
    def get(self, request, **kwargs):
        disciplines = models.PilotDiscipline.objects.all()
      
        # Render Technology Detail
        tmpl_disc = loader.get_template('warbook/pilotskill/pilot_disciplines.tmpl')
        
        body = Markup(tmpl_disc.generate(disciplines=disciplines, baseURL=request.get_full_path()))
        return HttpResponse(self.in_layout(body, request))


class DisciplineDetailView(ReferenceView):
    def get(self, request, discipline='', **kwargs):
    
        disciplineObject = get_object_or_404(models.PilotDiscipline, urlname=discipline)
        skills = models.PilotAbility.objects.filter(discipline=disciplineObject)
        
        tmpl_disc = loader.get_template('warbook/pilotskill/pilot_abilities.tmpl')
        
        body = Markup(tmpl_disc.generate(discipline=disciplineObject, abilities=skills))
        return HttpResponse(self.in_layout(body, request))