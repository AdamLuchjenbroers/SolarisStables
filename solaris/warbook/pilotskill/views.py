from django.views.generic import DetailView, ListView
from django.db.models import Q

from solaris.warbook.views import ReferenceViewMixin
from solaris.warbook.pilotskill import models

class DisciplineListView(ReferenceViewMixin, ListView):
    submenu_selected = 'Pilot Skills'
    template_name = 'warbook/pilotdisciplines.tmpl'
    model = models.PilotTraitGroup
    queryset = models.PilotTraitGroup.objects.filter(discipline_type__in=('T','S'))

class TraitDetailMixin(ReferenceViewMixin):
    def get_context_data(self, **kwargs):
        page_context = super(TraitDetailMixin, self).get_context_data(**kwargs)
        
        table = {}

        group = self.get_object()
        for trait in group.traits.all(): 
            if trait.table in table:
                table[trait.table].append(trait)
            else:
                table[trait.table] = [trait] 

        tupleset = []
        for key in table.keys():
            table[key].sort(key = lambda s: s.item)
            tupleset.append((key, table[key]))

        tupleset.sort(key = lambda x: x[0])
            
        page_context['table'] = tupleset

        return page_context
    
class DisciplineDetailView(TraitDetailMixin, DetailView):
    submenu_selected = 'Pilot Skills'
    template_name = 'warbook/pilotskilldetail.tmpl'
    slug_field = 'urlname__iexact' 
    model = models.PilotTraitGroup

class TraitsListView(ReferenceViewMixin, ListView):
    submenu_selected = 'Pilot Issues'
    template_name = 'warbook/pilotdisciplines.tmpl'
    model = models.PilotTraitGroup
    queryset = models.PilotTraitGroup.objects.filter(~Q(discipline_type='T'))

class TraitsDetailView(TraitDetailMixin, DetailView):
    submenu_selected = 'Pilot Issues'
    template_name = 'warbook/pilotskilldetail.tmpl'
    slug_field = 'urlname__iexact' 
    model = models.PilotTraitGroup
