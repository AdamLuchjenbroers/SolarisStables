from solaris.pdf import PDFView, SolarisDocTemplate, ReportSection
from .views import StableWeekMixin

from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.units import cm
from reportlab.platypus import Table, TableStyle, PageBreak

class StableDocTemplate(SolarisDocTemplate):
    def __init__(self, request, stable=None, stableweek=None, **kwargs):
        self.stable = stable
        self.stableweek = stableweek

        SolarisDocTemplate.__init__(self, request, **kwargs)

class OverviewReportSection(ReportSection):
    def __init__(self, stableweek, *args, **kwargs):
        self.stableweek = stableweek
        ReportSection.__init__(self, *args, **kwargs)

    def as_story(self):
        return []

class StablePDFReport(StableWeekMixin, PDFView):
    pagesize = landscape(A4)

    def get_report_name(self, *args, **kwargs):
        return 'Stable Owners Report - %s - Week %s' % (self.stable.stable_name, self.stableweek.week.week_number)

    def get(self, request, **kwargs):
        self.doc = StableDocTemplate(request
            , pagesize=landscape(A4)
            , report_name=self.get_report_name()
            , title=self.stable.stable_name
            , subtitle='Stable Owners Report - Week %i' % self.stableweek.week.week_number
        )

        story = []
        self.doc.build(story)
        return self.doc.get_response() 

