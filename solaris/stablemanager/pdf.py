from django.db.models import Sum

from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.units import cm
from reportlab.platypus import Table, TableStyle, PageBreak, Paragraph, KeepTogether, Spacer

from solaris import pdf_styles, pdf
from solaris.pdf import PDFView, SolarisDocTemplate, ReportSection
from solaris.stablemanager.ledger.pdf import LedgerReportSection
from solaris.stablemanager.pilots.pdf import RosterReportSection
from solaris.stablemanager.mechs.pdf import MechsReportSection
from solaris.stablemanager.repairs.pdf import RepairBillSection
from solaris.warbook.pilotskill.models import PilotRank

from .views import StableWeekMixin

class StableDocTemplate(SolarisDocTemplate):
    def __init__(self, request, stable=None, stableweek=None, **kwargs):
        self.stable = stable
        self.stableweek = stableweek

        if stable != None and stable.stable_bg != None:
            background = stable.stable_bg.path
        else:
            background = None

        SolarisDocTemplate.__init__(self, request, background=background, **kwargs)

class FinanceOverviewSubSection(pdf.ReportSubSection):
    def __init__(self, stableweek, name='Finances', key='ov-finances', level=1, **kwargs):
        self.stableweek = stableweek
        pdf.ReportSubSection.__init__(self, name, level, key=key)

    def as_story(self):
        story = self.story_header()

        finance_data = [
          ['Opening Balance', "{:,}".format(self.stableweek.opening_balance)]
        , ['Total Expenses', "{:,}".format(self.stableweek.total_spent())]
        , ['Total Income', "{:,}".format(self.stableweek.total_winnings())]
        , ['Total Assets', "{:,}".format(self.stableweek.total_assets())]
        , ['Current Balance', "{:,}".format(self.stableweek.closing_balance())]
        ]
        finance_style = [
          ('FONT', (0,0), (0,-1), 'Helvetica-Bold')
        , ('FONT', (-1,0), (-1,-1), 'Courier-Bold')
        , ('ALIGN', (-1,0), (-1,-1), 'RIGHT')
        , ('LINEABOVE', (0,-1), (-1,-1), 1, '#444444', 0)
        , ('LINEBELOW', (0,-1), (-1,-1), 2, '#000000', 0)
        ] 
        finance_table = Table(finance_data, [6*cm, 3*cm])
        finance_table.setStyle(TableStyle(finance_style))

        story.append(finance_table)
        story.append(Spacer(0, 0.5*cm))

        return [KeepTogether(story),]

class ProminenceOverviewSubSection(pdf.ReportSubSection):
    def __init__(self, stableweek, name='Prominence', key='ov-prominence', level=1, **kwargs):
        self.stableweek = stableweek
        pdf.ReportSubSection.__init__(self, name, level, key=key)

    def as_story(self):
        story = self.story_header()

        prominence_data = []
        for rank in PilotRank.objects.exclude(prominence_factor=0).order_by('-prominence_factor'):
            pilots = self.stableweek.pilots.filter(rank=rank) 

            for pw in self.stableweek.pilots.filter(rank=rank).exclude(fame=0):
                pilot_name = '%s - %s' % (rank.rank, pw.pilot)
               
                prominence_data.append(['%s - %s' % (rank.rank, pw.pilot), pw.fame * rank.prominence_factor])

        if self.stableweek.has_honoured():
            prominence_data.append(['Honoured Dead', self.stableweek.honoured.fame_value()])

        total_prominence = sum((row[1] for row in prominence_data))

        prominence_data.append(['Total Prominence', total_prominence])
        prominence_style = [
          ('FONT', (0,0), (0,-1), 'Helvetica-Bold')
        , ('ALIGN', (-1,0), (-1,-1), 'RIGHT')
        , ('LINEABOVE', (0,-1), (-1,-1), 1, '#444444', 0)
        , ('LINEBELOW', (0,-1), (-1,-1), 2, '#000000', 0)
        ] 
        prominence_table = Table(prominence_data, [6*cm, 3*cm])
        prominence_table.setStyle(TableStyle(prominence_style))

        story.append(prominence_table)
        story.append(Spacer(0, 0.5*cm))

        return [KeepTogether(story),]

class AssetsOverviewSubSection(pdf.ReportSubSection):
    def __init__(self, stableweek, name='Assets', key='ov-assets', level=1, **kwargs):
        self.stableweek = stableweek
        pdf.ReportSubSection.__init__(self, name, level, key=key)

    def as_story(self):
        story = self.story_header()

        assets_data = [
          ['Pilots', self.stableweek.pilots.all_present().exclude(prev_week=None).count()]
        , ['Non-Signature Mechs', self.stableweek.mechs.count_nonsignature()]
        ]

        total_assets = sum((row[1] for row in assets_data))
        assets_data.append(['Total Assets', total_assets])

        assets_style = [
          ('FONT', (0,0), (0,-1), 'Helvetica-Bold')
        , ('FONT', (-1,0), (-1,-1), 'Courier-Bold')
        , ('ALIGN', (-1,0), (-1,-1), 'RIGHT')
        , ('LINEABOVE', (0,-1), (-1,-1), 1, '#444444', 0)
        , ('LINEBELOW', (0,-1), (-1,-1), 2, '#000000', 0)
        ] 
        assets_table = Table(assets_data, [6*cm, 3*cm])
        assets_table.setStyle(TableStyle(assets_style))
        story.append(assets_table)

        if total_assets >= 28:
            story.append(Spacer(0, 0.5*cm))
            story.append(Paragraph('Both Exploded Management and Expanded Management actions are required', pdf_styles.indented_text))
        elif total_assets >= 25:
            story.append(Spacer(0, 0.5*cm))
            story.append(Paragraph('An Exploded Management action is required', pdf_styles.indented_text))
        elif total_assets >= 18:
            story.append(Spacer(0, 0.5*cm))
            story.append(Paragraph('An Expanded Management action is required', pdf_styles.indented_text))

        story.append(Spacer(0, 0.5*cm))

        return [KeepTogether(story),]

class OverviewReportSection(ReportSection):
    page_template = '2col'

    def __init__(self, stableweek, *args, **kwargs):
        self.stableweek = stableweek
        ReportSection.__init__(self, 'Overview', 0)


    def as_story(self):
        story = self.story_header()

        story += FinanceOverviewSubSection(self.stableweek).as_story()
        story += ProminenceOverviewSubSection(self.stableweek).as_story()
        story += AssetsOverviewSubSection(self.stableweek).as_story()

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
            , stable=self.stable
            , stableweek=self.stableweek
            , subtitle='Stable Owners Report - Week %i' % self.stableweek.week.week_number
        )

        story = []
        story += OverviewReportSection(self.stableweek).as_story()
        story += LedgerReportSection(self.stableweek, width=(A4[1]*0.8)).as_story()
        story += RosterReportSection(self.stableweek, width=(A4[1]*0.8)).as_story()
        story += MechsReportSection(self.stableweek).as_story()
        story += RepairBillSection(self.stableweek).as_story()

        self.doc.build(story)
        return self.doc.get_response() 

