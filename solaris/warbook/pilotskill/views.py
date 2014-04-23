from django_genshi import loader
from genshi import Markup
from solaris.warbook.pilotskill import models
from django.shortcuts import get_object_or_404
from solaris.core import render_page

def list_disciplines(request):
    disciplines = models.PilotDiscipline.objects.all()
  
    # Render Technology Detail
    tmpl_disc = loader.get_template('warbook/pilotskill/pilot_disciplines.tmpl')
    
    body = Markup(tmpl_disc.generate(disciplines=disciplines))
    return render_page(body=body, selected='^^^^', request=request) 

def show_discipline(request, discipline=''):
    
    disciplineObject = get_object_or_404(models.PilotDiscipline, urlname=discipline)
    skills = models.PilotAbility.objects.filter(discipline=disciplineObject)
    
    tmpl_disc = loader.get_template('warbook/pilotskill/pilot_abilities.tmpl')
    
    body = Markup(tmpl_disc.generate(discipline=disciplineObject,abilities=skills))
    return render_page(body=body, selected='^^^^', request=request) 