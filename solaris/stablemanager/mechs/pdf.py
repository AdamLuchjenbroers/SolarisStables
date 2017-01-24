from reportlab.platypus import Spacer, KeepTogether
from reportlab.platypus.flowables import Flowable
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.units import cm, mm

from solaris import pdf_styles
from solaris.pdf import PDFView, Heading, ReportSection, ReportSubSection, rounded_rect
from solaris.stablemanager.views import StableWeekMixin

class MechChit(Flowable):
    def __init__(self, mech):
        self.mech = mech

    def wrap(self, *args):
        return (12*cm, 2.2*cm)

    def draw(self):
        self.canv.setLineWidth(1*mm)
        rounded_rect(self.canv, 11*cm, 2*cm, 4*mm, x=0.5*cm) 
        self.canv.line(3*cm, 0.2*cm, 3*cm, 1.8*cm)

        self.canv.setFont('Helvetica', 36)
        self.canv.drawRightString(2.8*cm, 0.6*cm, '%d' % self.mech.tonnage)

        self.canv.setFont('Helvetica', 18)
        self.canv.drawString(3.4*cm, 1.1*cm, '%s %s' % (self.mech.mech_name, self.mech.mech_code))

        self.canv.setFont('Helvetica', 12)
        self.canv.drawString(3.4*cm, 0.4*cm, 'BV: %d, Credits: %d' % (self.mech.bv_value, self.mech.credit_value))

class SignatureReportSection(ReportSubSection):
    def __init__(self, stableweek, name='Signature Mechs', level=1):
        self.stableweek = stableweek
        ReportSubSection.__init__(self, name, level)

    def as_story(self):
        pilots = self.stableweek.get_sigmech_pilots()

        if pilots.count() < 1:
            return []

        story = self.story_header()
        for pw in pilots:
            pilot_story = [(Heading('%s' % pw.pilot, pdf_styles.headings[self.level+1]))]
            for smw in pw.signature_mechs():
                pilot_story.append(MechChit(smw.current_design))

            story.append(KeepTogether(pilot_story))
            story.append(Spacer(0,0.3*cm)) 

        return [KeepTogether(story)]

class NonSignatureReportSection(ReportSubSection):
    def __init__(self, stableweek, name='Non-Signature Mechs', level=1):
        self.stableweek = stableweek
        ReportSubSection.__init__(self, name, level)

    def as_story(self):
        groups = ( 
          ('Light'   ,{'current_design__tonnage__lt'  : 40} )
        , ('Medium'  ,{'current_design__tonnage__gte' : 40, 'current_design__tonnage__lt' : 60} )
        , ('Heavy'   ,{'current_design__tonnage__gte' : 40, 'current_design__tonnage__lt' : 80} )
        , ('Assault' ,{'current_design__tonnage__gte' : 80} )
        )

        non_sig = self.stableweek.mechs.non_signature()

        if non_sig.count() < 1:
            return []
        story = self.story_header()

        for (name, filter_args) in groups:
            group = []
            qs = non_sig.filter(**filter_args)

            if qs.count() < 1:
                continue

            group.append(Heading(name, pdf_styles.headings[self.level+1]))
            for smw in qs:
                group.append(MechChit(smw.current_design))
            story.append(KeepTogether(group))
            story.append(Spacer(0,0.3*cm)) 
        return story

class OrderedMechsReportSection(ReportSubSection):
    def __init__(self, stableweek, name='On Order', level=1):
        self.stableweek = stableweek
        ReportSubSection.__init__(self, name, level)

    def as_story(self):
        mechs = self.stableweek.mechs.on_order()
        
        if mechs.count < 1:
            return []

        story = self.story_header()
        for smw in mechs:
            story.append(MechChit(smw.current_design))
        
        return [KeepTogether(story)]

class MechsReportSection(ReportSection):
    page_template = '2col'

    def __init__(self, stableweek, name='Available Mechs', level=0, width=(A4[0]*0.8)):
        self.stableweek = stableweek
        self.name = name
        self.level = level
         
    def as_story(self):
        story = self.story_header()

        story += NonSignatureReportSection(self.stableweek, level=self.level+1).as_story()
        story += SignatureReportSection(self.stableweek, level=self.level+1).as_story()
        story += OrderedMechsReportSection(self.stableweek, level=self.level+1).as_story()

        return story

class MechListPDFView(StableWeekMixin, PDFView):

    def get_report_name(self, *args, **kwargs):
        return '%s - BattleMechs Week %2d' % (self.stable.stable_name, self.stableweek.week.week_number)

    def get(self, request, *args, **kwargs):
        self.doc = SolarisDocTemplate(request, pagesize=landscape(A4), report_name=self.get_report_name())

        report = MechsReportSection(self.stableweek)

        self.doc.build(report.as_story())
        return self.doc.get_response()
