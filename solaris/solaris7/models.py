from django.db import models
from django.conf import settings
from django.core.urlresolvers import reverse

class SolarisCampaign(models.Model):
    campaign = models.ForeignKey('campaign.Campaign')

    initial_balance = models.IntegerField()
    initial_contracts = models.ManyToManyField('warbook.Technology')
    actions_startweek = models.IntegerField(default=10)
    actions_duringweek = models.IntegerField(default=10)

    def current_week(self):
        return self.weeks.get(next_week=None)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = 'Solaris 7 Campaign'
        db_table = 'solaris7_campaign'
        app_label = 'solaris7'
    

class Zodiac(models.Model):
    sign = models.CharField(max_length = 20)
    rules = models.TextField()
    next = models.OneToOneField('Zodiac', related_name='prev', null=True)
    campaign = models.ForeignKey(SolarisCampaign, null=True, blank=True)

    class Meta:
        verbose_name = 'Zodiac Sign'
        db_table = 'solaris7_zodiac'
        app_label = 'solaris7'
    
    def __unicode__(self):
        return self.sign

class BroadcastWeekManager(models.Manager):
    def current_week(self):
        return super(BroadcastWeekManager,self).get(next_week=None)

class BroadcastWeek(models.Model):
    week_number = models.IntegerField()
    sign = models.ForeignKey(Zodiac)
    next_week = models.OneToOneField('BroadcastWeek', on_delete=models.SET_NULL, null=True, blank=True, related_name='prev_week')
    campaign = models.ForeignKey(SolarisCampaign, related_name="weeks")
    week_started = models.BooleanField(default=False)
  
    objects = BroadcastWeekManager()  

    def start_week(self):
        self.week_started = True
        self.save()

    def reset_week(self):
        self.week_started = False
        self.save()

    def __unicode__(self):
        return 'Week %i' % self.week_number
        
    class Meta:
        verbose_name = 'Broadcast Week'
        db_table = 'solaris7_broadcastweek'
        app_label = 'solaris7'

    def has_prev_stables(self):
        return (hasattr(self, 'prev_week') and self.prev_week.stableweek_set.count() > 0)

    def list_waiting_stables(self):
        from solaris.stablemanager.models import Stable
        return Stable.objects.exclude(ledger__week=self)

    def list_techs_available(self):
        if hasattr(self, 'prev_week') and self.prev_week.stableweek_set.count() > 0:
            from solaris.warbook.techtree.models import Technology 

            tech_list = Technology.objects.none()

            for stable in self.prev_week.stableweek_set.all():
                tech_list |= stable.supply_contracts.all()

            return tech_list.distinct().order_by('tier', 'name')
        else:
            return self.campaign.initial_contracts.all().order_by('tier', 'name')

    def list_techs_all_have(self):
        if hasattr(self, 'prev_week') and self.prev_week.stableweek_set.count() > 0:
            from solaris.warbook.techtree.models import Technology 

            tech_list = Technology.objects.all()

            for stable in self.prev_week.stableweek_set.all():
                tech_list &= stable.supply_contracts.all()

            return tech_list.distinct().order_by('tier', 'name')
        else:
            return self.campaign.initial_contracts.all().order_by('tier', 'name')

    def advance(self):
        if self.next_week == None:            
            self.next_week = BroadcastWeek.objects.create(
                week_number = self.week_number + 1
              , sign = self.sign.next
              , campaign = self.campaign
            )
            self.save()
        
        return self.next_week

    def has_prev_week(self):
       return hasattr(self, 'prev_week')
            
    def get_absolute_url(self):
        return reverse('campaign_overview', kwargs={'week': self.week_number})

def createInitialPilots(stable):
    from solaris.stablemanager.pilots.models import Pilot, PilotWeek

    templates = stable.campaign.initial_pilots.all()
    week = stable.get_stableweek()
    
    for t in templates:
        for i in range(0,t.count):
            pilot = Pilot.objects.create(
                stable = stable
            ,   pilot_callsign = 'Unnamed %s %i' % (t.rank.rank, i+1)
            ,   affiliation = stable.house
            )
            PilotWeek.objects.create(
                pilot = pilot
            ,   week = week
            ,   rank = t.rank
            ,   skill_gunnery = t.gunnery
            ,   skill_piloting = t.piloting
            ,   fame = t.fame  
            )

class StartingPilotTemplate(models.Model):
    campaign = models.ForeignKey(SolarisCampaign, related_name='initial_pilots')

    count = models.IntegerField()
    rank = models.ForeignKey('warbook.PilotRank')
    piloting = models.IntegerField()
    gunnery = models.IntegerField()
    fame = models.IntegerField(default=0)
        
    class Meta:
        verbose_name = 'Starting Pilot Template'
        db_table = 'solaris7_pilottemplate'
        app_label = 'solaris7'
