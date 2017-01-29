from django.views.generic import View, TemplateView, ListView, FormView
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.http import HttpResponse 

import json
from urllib import unquote

from solaris.warbook.pilotskill.models import PilotRank, TrainingCost, PilotTrait
from solaris.stablemanager.views import StableViewMixin, StableWeekMixin
from solaris.stablemanager.mechs.models import StableMechWeek

from . import forms, models

class StablePilotMixin(StableWeekMixin):
    submenu_selected = 'Pilots'
    model = models.PilotWeek    
    view_url_name = 'stable_pilots'

    def get_queryset(self):
        return self.stableweek.pilots.all_present()

class PilotWeekMixin(StableWeekMixin):
    def dispatch(self, request, week=None, callsign=None, *args, **kwargs):
        redirect = self.get_stable(request)
        if redirect:
            return redirect

        self.get_stableweek()

        if callsign != None:
            pass
        elif request.method == 'POST':
            callsign = request.POST['callsign']
        else:
            callsign = request.GET['callsign']

        try:
            self.pilot = models.Pilot.objects.get(pilot_callsign=unquote(callsign), stable=self.stable)
            self.pilotweek = models.PilotWeek.objects.get(pilot=self.pilot, week=self.stableweek)
        except KeyError:
            return HttpResponse('Incomplete AJAX request', status=400)
        except ValueError:
            return HttpResponse('Invalid AJAX request', status=400)
        except models.Pilot.DoesNotExist:
            return HttpResponse('Unrecognised Callsign', status=404)
        except models.PilotWeek.DoesNotExist:
            return HttpResponse('Cannot find Pilot Week', status=404)

        return super(PilotWeekMixin, self).dispatch(request, *args, **kwargs)

class StablePilotsView(StablePilotMixin, ListView):
    template_name = 'stablemanager/stable_pilots.tmpl'

    def get_context_data(self, **kwargs):
        page_context = super(StablePilotsView, self).get_context_data(**kwargs)

        available_disciplines = self.stable.stable_disciplines.all() | self.stable.house.house_disciplines.all()
        page_context['available_disciplines'] = available_disciplines.distinct().order_by('name')

        page_context['training_form'] = forms.PilotTrainingForm(stableweek=self.stableweek, auto_id='pilot-training-%s')
        page_context['trait_form'] = forms.PilotTraitForm(stableweek=self.stableweek, auto_id='pilot-trait-%s')
        page_context['cure_form'] = forms.PilotRemoveTraitForm(stableweek=self.stableweek, auto_id='pilot-cure-%s')
        page_context['defer_form'] = forms.PilotDefermentForm(stableweek=self.stableweek, auto_id='pilot-defer-%s')

        dead = self.stableweek.pilots.all_dead()
        if dead.count() > 0:
            page_context['honoured_form'] = forms.HonouredDeadForm(stableweek=self.stableweek, auto_id='honoured-dead-%s')

        return page_context

class StablePilotsListPartView(StablePilotMixin, ListView):
    template_name = 'stablemanager/fragments/stable_pilot_list.html'

class StablePilotsTrainingPartView(StablePilotMixin, ListView):
    template_name = 'stablemanager/fragments/training_list.html'

class StablePilotsTraitsPartView(StablePilotMixin, ListView):
    template_name = 'stablemanager/fragments/trait_list.html'

class StablePilotsDeferredPartView(StablePilotMixin, ListView):
    template_name = 'stablemanager/fragments/deferred_list.html'

class StableHonouredDeadPartView(StablePilotMixin, ListView):
    template_name = 'stablemanager/fragments/honoured_dead.html'

    def get_context_data(self, **kwargs):
        page_context = super(StableHonouredDeadPartView, self).get_context_data(**kwargs)

        dead = self.stableweek.pilots.all_dead()
        if dead.count() > 0:
            page_context['honoured_form'] = forms.HonouredDeadForm(stableweek=self.stableweek, auto_id='honoured-dead-%s')

        return page_context
        
class InitialPilotNamingView(StableViewMixin, FormView):
    template_name = 'stablemanager/initial_pilots.tmpl'
    form_class = forms.PilotNamingFormSet
    success_url = '/stable'

    def get_form_kwargs(self):
        kwargs = super(InitialPilotNamingView, self).get_form_kwargs()
        if self.request.method == 'GET':
            kwargs['queryset'] = self.stable.pilots.filter(pilot_callsign__startswith='Unnamed')

        return kwargs

    def form_valid(self, form):
        for pilot in form:
            pilot.instance.save()

        return super(InitialPilotNamingView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        page_context = super(InitialPilotNamingView, self).get_context_data(**kwargs)
        
        page_context['submit'] = 'Rename All'
        return page_context

class StablePilotFormAbstract(TemplateView):
    template_name = 'stablemanager/forms/add_pilot.html'

    def get_context_data(self, **kwargs):
        page_context = super(StablePilotFormAbstract, self).get_context_data(**kwargs)

        page_context['pilotform'] = self.pilotform
        page_context['pilotweekform'] = self.pilotweekform
        page_context['trainingform'] = self.trainingformset
        page_context['problemform'] = self.problemformset

        page_context['is_edit_form'] = self.__class__.is_edit_form

        return page_context


class StableAddPilotFormView(StableWeekMixin, StablePilotFormAbstract):
    is_edit_form = False

    def get(self, request, week=None):
        self.pilotform = forms.PilotForm(None, prefix='pilot', stable=self.stable)
        self.pilotweekform = forms.PilotWeekForm(prefix='pweek')
        self.trainingformset = forms.PilotTrainingFormSet(prefix='train') 
        self.problemformset = forms.PilotTraitFormSet(prefix='issue') 
       
        return super(StableAddPilotFormView, self).get(request, week=week)

    def post(self, request, week=None):
        self.pilotform = forms.PilotForm(request.POST, prefix='pilot', stable=self.stable)
        self.pilotweekform = forms.PilotWeekForm(request.POST, prefix='pweek')
        self.trainingformset = forms.PilotTrainingFormSet(request.POST, prefix='train') 
        self.problemformset = forms.PilotTraitFormSet(request.POST, prefix='issue') 

        if self.pilotform.is_valid() and self.pilotweekform.is_valid() \
        and self.trainingformset.is_valid() and self.problemformset.is_valid():
            self.pilotform.save(commit=False)
            pilot = self.pilotform.instance
            pilot.stable = self.stable
            pilot.save()

            self.pilotweekform.save(commit = False) 
            pilotweek = self.pilotweekform.instance 
            pilotweek.pilot = self.pilotform.instance
            pilotweek.week = self.stableweek
            pilotweek.save()

            self.trainingformset.instance = pilotweek
            self.trainingformset.save()

            self.problemformset.instance = pilotweek
            self.problemformset.save()

            pilotweek.cascade_advance()

            return HttpResponse('Pilot Added', status=201)
        else:
            return super(StableAddPilotFormView, self).get(request, week=week)
 
class StableEditPilotFormView(PilotWeekMixin, StablePilotFormAbstract):
    is_edit_form = True

    def get(self, request, week=None, callsign=None):
        self.pilotform = forms.PilotForm(None, prefix='pilot', stable=self.stable, instance=self.pilot)
        self.pilotweekform = forms.PilotWeekForm(prefix='pweek', instance=self.pilotweek)
        self.trainingformset = None
        self.problemformset = None 
       
        return super(StableEditPilotFormView, self).get(request, week=week)

    def post(self, request, week=None, callsign=None):
        self.pilotform = forms.PilotForm(request.POST, prefix='pilot', stable=self.stable, instance=self.pilot)
        self.pilotweekform = forms.PilotWeekForm(request.POST, prefix='pweek', instance=self.pilotweek)
        self.trainingformset = None
        self.problemformset = None 

        if self.pilotform.is_valid() and self.pilotweekform.is_valid():
            self.pilotform.save()
            self.pilotweekform.save()

            if self.pilotweekform.cleaned_data['remove'] == 'remove':
                self.pilotweekform.instance.set_removed(True)

            return HttpResponse('Pilot Changed', status=201)
        else:
            return super(StableEditPilotFormView, self).get(request, week=week)

class AjaxSetTrainingPoints(StableWeekMixin, View):
    def post(self, request, week=None):
        try:
            self.stableweek.training_points = int(request.POST['training-points'])
            self.stableweek.save()

            result = {
              'rookie-tp'    : self.stableweek.rookie_tp()
            , 'contender-tp' : self.stableweek.contender_tp()
            , 'total-tp'     : self.stableweek.training_points
            }

            return HttpResponse(json.dumps(result))
        except KeyError:
            return HttpResponse('Incomplete AJAX request', status=400)
        except ValueError:
            return HttpResponse('Invalid AJAX request', status=400)

class AjaxPilotMixin(PilotWeekMixin, View):
    def dispatch(self, request, *args, **kwargs):
        # Wrap all requests with this exception handler so handling of missing or 
        # incorrect query parameters is consistent
        try:
            return super(AjaxPilotMixin, self).dispatch(request, *args, **kwargs)
        except KeyError:
            return HttpResponse('Incomplete AJAX request', status=400)
        except ValueError:
            return HttpResponse('Invalid AJAX request', status=400)

class AjaxSetPilotAttribute(AjaxPilotMixin, View):
    def post(self, request, week=None):
        attribute = request.POST['attribute']
        value = int(request.POST['value']) 
        if attribute == 'cp':
            self.pilotweek.adjust_character_points = value
        elif attribute == 'tp':
            self.pilotweek.assigned_training_points = value
        elif attribute == 'wounds':
            value = self.pilotweek.set_wounds(value)
        elif attribute == 'fame':
            value = self.pilotweek.set_fame(value)
        elif attribute == 'blackmark':
            value = self.pilotweek.set_blackmarks(value)
        else:
            return HttpResponse('Unrecognised Attribute: %s' % attribute, status=400)

        self.pilotweek.save()

        result = {
          'callsign' : self.pilot.pilot_callsign
        , 'value'    : value
        , 'total-cp' : self.pilotweek.character_points()
        , 'is-dead'  : self.pilotweek.is_dead()
        , 'tp-table' : self.pilotweek.week.assigned_tp_counts()
        }
        return HttpResponse(json.dumps(result))

class AjaxSetPilotStatus(AjaxPilotMixin, View):
    def post(self, request, week=None):
        new_status = request.POST['status']

        if new_status in ('X', '-', 'R'):
            self.pilotweek.status = new_status
            self.pilotweek.save()

            result = {
              'callsign' : self.pilot.pilot_callsign
            , 'status'   : self.pilotweek.status
            }
            return HttpResponse(json.dumps(result))
        else:
            return HttpResponse('%s is not a valid status code' % new_status, status=400)

class AjaxGetAvailableTraining(AjaxPilotMixin, View):
    def get(self, request, week=None):
        gunnery_training = self.pilotweek.next_gunnery() 
        piloting_training = self.pilotweek.next_piloting()
        skills_training = self.pilotweek.next_skills()

        options = {
          'gunnery'  : { 'cost' : gunnery_training.cost, 'skill' : gunnery_training.train_to 
                       , 'available' : (self.pilotweek.character_points() >= gunnery_training.cost)  }
        , 'piloting' : { 'cost' : piloting_training.cost, 'skill' : piloting_training.train_to 
                       , 'available' : (self.pilotweek.character_points() >= piloting_training.cost)  }
        , 'skills'   : { 'cost' : skills_training.cost, 'skill' : skills_training.train_to 
                       , 'available' : (self.pilotweek.character_points() >= skills_training.cost)  }
        }
        return HttpResponse(json.dumps(options))

class AjaxGetPilotSkillsList(AjaxPilotMixin, View):
    def get(self, request, week=None):
        disciplines = self.stable.stable_disciplines.all() | self.stable.house.house_disciplines.all()

        skill_list = {}
        for group in disciplines:
            if not self.pilotweek.has_discipline(group):
                skill_list[group.name] = [ { 'id' : skill.id, 'name' : skill.name } for skill in group.traits.all()]

        return HttpResponse(json.dumps(skill_list))

class AjaxGetCurrentPilotTraits(AjaxPilotMixin, View):
    def get(self, request, week=None):
        traits = self.pilotweek.traits.exclude(trait__discipline__discipline_type='T')
        trait_list = [ { 'id' : t.trait.id, 'name' : t.trait.name } for t in traits ]

        return HttpResponse(json.dumps(trait_list))

class AjaxAddPilotTraining(AjaxPilotMixin, View):
    def post(self, request, week=None):
        try:
            (train_type, skill) = request.POST['training'].split('|')
            train_cost = TrainingCost.objects.get(training=train_type, train_to=int(skill))
 
            (training, created) = models.PilotTrainingEvent.objects.get_or_create(pilot_week=self.pilotweek, training=train_cost)
            if 'skill' in request.POST:
                skill = PilotTrait.objects.get(id=int(request.POST['skill']))
                if request.POST['notes'] != "":
                    notes = request.POST['notes']
                else:
                    notes = None

                training.trait = skill
                training.notes = notes    

            training.save()        
            self.pilotweek.save()

            result = self.pilotweek.state_parcel()
            return HttpResponse(json.dumps(result))
        except PilotTrait.DoesNotExist:
            return HttpResponse('Invalid Skill ID', status=400)
        except TrainingCost.DoesNotExist:
            return HttpResponse('Malformed Training Type ID', status=400)

class AjaxAddPilotTrait(AjaxPilotMixin, View):
    def post(self, request, week=None):
        try:
            trait = PilotTrait.objects.get(id=int(request.POST['trait']))

            if request.POST['notes'] != "":
                notes = request.POST['notes']
            else:
                notes = None

            (gain_trait, created) = models.PilotTraitEvent.objects.get_or_create(pilot_week=self.pilotweek, trait=trait)
            gain_trait.notes = notes
            gain_trait.save()

            self.pilotweek.save()

            result = self.pilotweek.state_parcel()
            return HttpResponse(json.dumps(result))

        except PilotTrait.DoesNotExist:
            return HttpResponse('Invalid Trait ID', status=400)

class AjaxCurePilotTrait(AjaxPilotMixin, View):
    def post(self, request, week=None):
        try:
            trait = PilotTrait.objects.get(id=int(request.POST['trait']))

            (gain_trait, created) = models.PilotTraitEvent.objects.get_or_create(pilot_week=self.pilotweek, trait=trait)
            gain_trait.added = False
            gain_trait.save()

            self.pilotweek.save()

            result = self.pilotweek.state_parcel()
            return HttpResponse(json.dumps(result))

        except PilotTrait.DoesNotExist:
            return HttpResponse('Invalid Trait ID', status=400)

class AjaxRemovePilotEventBase(AjaxPilotMixin, View):
    def get_trainevent(self, request):
        return None
        return self.pilotweek.training.get(id=int(request.POST['train_id']))

    def post(self, request, week=None):
        try:
            train = self.get_trainevent(request) 
            self.pilotweek.remove_trait(train.trait)
            train.delete()

            self.pilotweek.save()
    
            result = self.pilotweek.state_parcel()
            return HttpResponse(json.dumps(result))
        except models.PilotTrainingEvent.DoesNotExist:
            return HttpResponse('Training Event Does Not Exist', status=404)
        except models.PilotTraitEvent.DoesNotExist:
            return HttpResponse('Trait Event Does Not Exist', status=404)

class AjaxRemovePilotTraining(AjaxRemovePilotEventBase):
    def get_trainevent(self, request):
        return self.pilotweek.training.get(id=int(request.POST['train_id']))

class AjaxRemovePilotTrait(AjaxRemovePilotEventBase):
    def get_trainevent(self, request):
        return self.pilotweek.new_traits.get(id=int(request.POST['trait_id']))

class AjaxAddPilotDeferred(AjaxPilotMixin, View):
    def post(self, request, week=None):
        try: 
            trait = PilotTrait.objects.get(id=int(request.POST['trait']))
            duration = int(request.POST['duration'])

            if request.POST['notes'] != "":
                notes = request.POST['notes']
            else:
                notes = None

            (deferred, created) = models.PilotDeferment.objects.get_or_create(pilot_week=self.pilotweek, deferred=trait)
            deferred.duration = duration
            deferred.notes = notes
            deferred.save()

            result = self.pilotweek.state_parcel()
            return HttpResponse(json.dumps(result))
        except PilotTrait.DoesNotExist:
            return HttpResponse('Invalid Trait ID', status=400)

class AjaxEndPilotDeferred(AjaxPilotMixin, View):
    def post(self, request, week=None):
        try:
            defer = self.pilotweek.deferred.get(id=int(request.POST['defer_id']))
            defer.end_deferment()

            result = self.pilotweek.state_parcel()
            return HttpResponse(json.dumps(result))
        except models.PilotDeferment.DoesNotExist:
            return HttpResponse('Invalid Deferment ID', status=400)

class AjaxListHonouredSignatures(AjaxPilotMixin, View):
    def get(self, request, week=None):
        sig_mechs_list = ({'smw_id' : smw.id, 'name' : str(smw.current_design)} for smw in self.pilotweek.signature_mechs.all())
       
        return HttpResponse(json.dumps(sig_mechs_list))

class AjaxAddHonouredDead(AjaxPilotMixin, View):
    def post(self, request, week=None):
        if 'display_id' in request.POST:
            display_mech = StableMechWeek.objects.get(id=int(request.POST['display_id']))
        else:
            display_mech = None

        honours = self.pilotweek.honour_dead(display_mech=display_mech)
        return HttpResponse(json.dumps(honours.state_parcel()))

class AjaxRemoveHonouredDead(StableWeekMixin, View):
    def post(self, request, week=None):
        try:
            honoured = models.HonouredDead.objects.get(id=int(request.POST['honoured_id']))

            if honoured.week == self.stableweek:
                honoured.delete()
                return HttpResponse(json.dumps(True))
            else:
                return HttpResponse('Honoured Dead Not Owned By Stable', status=403)
        except KeyError:
            return HttpResponse('Incomplete AJAX request', status=400)
        except ValueError:
            return HttpResponse('Invalid AJAX request', status=400)
        except models.HonouredDead.DoesNotExist:
            return HttpResponse('Honoured Dead Record Does Not Exist', status=404) 
