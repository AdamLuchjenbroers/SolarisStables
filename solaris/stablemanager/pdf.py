from solaris.pdf import PDFView, SolarisDocTemplate, ReportSection
from .views import StableWeekMixin

from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.units import cm
from reportlab.platypus import Table, TableStyle, PageBreak, Paragraph

from solaris import pdf_styles, pdf
from solaris.stablemanager.ledger.pdf import LedgerReportSection

class StableDocTemplate(SolarisDocTemplate):
    def __init__(self, request, stable=None, stableweek=None, **kwargs):
        self.stable = stable
        self.stableweek = stableweek

        SolarisDocTemplate.__init__(self, request, **kwargs)

class OverviewReportSection(ReportSection):
    page_template = '2col'

    def __init__(self, stableweek, *args, **kwargs):
        self.stableweek = stableweek
        ReportSection.__init__(self, 'Overview', 0)


    def as_story(self):
        story = self.story_header()

        finances_data = [
          ('Current Balance', self.stableweek.closing_balance())
        , ('Total Expenses', self.stableweek.total_spent())
        , ('Total Income', self.stableweek.total_winnings())
        , ('Total Assets', self.stableweek.total_assets())
        ] 
        finances = pdf.ListSubsection('Finances', self.level + 1, finances_data)

        story += finances.as_story()

        return story

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
        story += OverviewReportSection(self.stableweek).as_story()
        story += LedgerReportSection(self.stableweek, width=(A4[1]*0.8)).as_story()

        self.doc.build(story)
        return self.doc.get_response() 

