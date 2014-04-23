from django_genshi import loader
from genshi import Markup
from solaris.warbook.pilotskill import models
from solaris.core import render_page

def list_disciplines(request):
    disciplines = models.PilotDiscipline.objects.all()
  
    # Render Technology Detail
    tmpl_tech = loader.get_template('warbook/pilotskill/pilot_disciplines.tmpl')
    
    body = Markup(tmpl_tech.generate(disciplines=disciplines))
    return render_page(body=body, selected='^^^^', request=request) 

def show_discipline(request, discipline=''):
    #discipline = models.PilotDiscipline.objects.filter(name=discipline)
    #skills = models.PilotAbility.objects.filter(discipline=discipline[0])
    
    body = Markup('<p>TODO: List Discipline Skills Here</p>')
    return render_page(body=body, selected='^^^^', request=request) 