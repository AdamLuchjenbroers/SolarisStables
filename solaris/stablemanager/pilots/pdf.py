from reportlab.platypus import Table, TableStyle
from reportlab.platypus.flowables import Flowable
from reportlab.lib.pagesizes import A4

from solaris.pdf import PDFView, ReportSection, SolarisDocTemplate
from solaris.stablemanager.views import StableWeekMixin

from reportlab.lib.units import cm

class WoundIndicator(Flowable):
    def __init__(self, wounds, marks):
        self.wounds = wounds
        self.marks = marks 

    def wrap(self, availWidth, availHeight):
        if (availWidth / 6.0) < availHeight:
            self.icon_size = availWidth / 6.0
        else:
            self.icon_size = float(availHeight)

        return (self.icon_size * 6), self.icon_size

    def draw(self):
	self.canv.setFillColor('#666666')
        self.canv.setLineWidth(1)

        y = 0.5 * self.icon_size
        rad = 0.4 * self.icon_size

        for wound in range(6):
            x = (wound + 0.5) * self.icon_size
            fill = (self.wounds > wound) or (self.marks >= (6 - wound))

            self.canv.circle(x, y, rad, fill=fill)
         

class RosterReportSection(ReportSection):
    def __init__(self, stableweek, name='Roster', level=0, width=(A4[0]*0.8)):
        self.stableweek = stableweek
        self.name = name
        self.level = level

    def as_story(self):
        roster_data = [['Pilot', 'Rank', 'Fame', 'Abilities', 'Skills', 'BV', 'XP', 'Wounds']]
        roster_style = [('BACKGROUND', (0,0), (-1,0), '#CCCCCC')
                       ,('LINEABOVE', (0,0), (-1,0), 4, '#000000')
                       ,('ALIGN', (-1,0), (-1,-1), 'RIGHT')]

        roster_widths = [width * cm for width in (6,2,2,3,8,1,1,3)]

        for pilot in self.stableweek.pilots.all_present():
            roster_data.append([
              pilot.pilot.full_name()
            , pilot.rank
            , pilot.fame
            , '%d / % d' % (pilot.skill_gunnery, pilot.skill_piloting)
            , ', '.join((trait.trait.name for trait in pilot.traits.all()))
            , pilot.bv()
            , pilot.character_points()
            , WoundIndicator(pilot.wounds, pilot.blackmarks)
            ])

        roster_table = Table(roster_data, roster_widths)
        roster_table.setStyle(TableStyle(roster_style))

        story = self.story_header()
        story.append(roster_table)
        return(story)

class RosterPDFView(StableWeekMixin, PDFView):

    def get_report_name(self, *args, **kwargs):
        return '%s - Stable Roster Week %2d' % (self.stable.stable_name, self.stableweek.week.week_number)

    def get(self, request, *args, **kwargs):
        self.doc = SolarisDocTemplate(request, pagesize=landscape(A4), report_name=self.get_report_name())

        report = RosterReportSection(self.stableweek)

        self.doc.build(report.as_story())

