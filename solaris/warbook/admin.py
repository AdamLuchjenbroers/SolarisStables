from django.contrib import admin
import solaris.warbook.techtree.models as tech_models
import solaris.warbook.techtree.admin as tech_admin

import solaris.warbook.pilotskill.models as pilot_models
import solaris.warbook.pilotskill.admin as pilot_admin

import solaris.warbook.models as base_models

# Import Houses
admin.site.register(base_models.House)

# Import Techtree
admin.site.register(tech_models.Technology, tech_admin.TechnologyAdmin)

# Import Pilot Skills and Disciplines
admin.site.register(pilot_models.PilotDiscipline, pilot_admin.PilotDisciplineAdmin)
admin.site.register(pilot_models.PilotTrait, pilot_admin.PilotTraitAdmin)

