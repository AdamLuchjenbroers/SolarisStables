#from django.http import HttpResponse
from django_genshi import loader
from genshi import Markup
from django.shortcuts import get_object_or_404
from django.http import HttpResponse

from solaris.warbook.techtree import models
from solaris.warbook.views import ReferenceView

class TechnologyListView(ReferenceView):
    def get(self, request, **kwargs):
        
        # Construct Technologies list
        tech_list = []
        
        for (code, name) in models.Technology.categories:
            tech_list.append(
                ( name, [(tier, models.Technology.objects.filter(category=code, tier=tier, show=True)) for tier in range(1,4)] )
            )
    
        # Render Technologies List
        tmpl_tech = loader.get_template('warbook/techtree/tech_list.tmpl')    
        techtree = Markup(tmpl_tech.generate(techtree=tech_list, baseURL=request.get_full_path()))

        return HttpResponse(self.in_layout(techtree, request))

class TechnologyDetailView(ReferenceView):
    def get(self, request, technology='', **kwargs):
        # Get Technology Information
        techdata = get_object_or_404(models.Technology, urlname=technology)
        modifiers = models.TechnologyRollModifier.objects.filter(technology=techdata)

        # Render Technology Detail
        tmpl_tech = loader.get_template('warbook/techtree/tech_detail.tmpl')
        description = Markup(techdata.description)
    
        body = Markup(tmpl_tech.generate(description=description, tech=techdata, modifiers=modifiers))
    
        return HttpResponse(self.in_layout(body, request))