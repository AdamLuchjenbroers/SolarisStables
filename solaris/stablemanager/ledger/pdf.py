from reportlab.platypus import Table, TableStyle, BaseDocTemplate, Frame, PageTemplate
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape

from django.db import models
from django.http import HttpResponse 

from solaris.pdf import PDFView, ReportSection, SolarisDocTemplate
from solaris.stablemanager.views import StableWeekMixin
from solaris import pdf_styles

from .models import LedgerItem

class LedgerReportSection(ReportSection):
    def __init__(self, stableweek, name='Ledger', level=0, width=(A4[0]*0.8)):
        self.stableweek = stableweek
        self.name = name
        self.level = level

        self.col_widths = [width * 0.7, width * 0.3]

    def as_story(self):
        ledger_data = [ ['Opening Balance', "{:,}".format(self.stableweek.opening_balance)]]
        ledger_style = [('BACKGROUND', (0,0), (-1,0), '#CCCCCC')
                       ,('FONT', (0,0), (-1,0), 'Courier-Bold')
                       ,('LINEABOVE', (0,0), (-1,0), 4, '#000000')
                       ,('ALIGN', (-1,0), (-1,-1), 'RIGHT')]

        for (code, description) in LedgerItem.item_types:
            entries = self.stableweek.entries.filter(type=code)
            if entries.count() < 1: 
                continue

            ledger_data.append([description, None])
            row = len(ledger_data)-1
            ledger_style.append(['LINEABOVE',(0,row),(-1,row), 2, '#000000'])
            ledger_style.append(['LINEBELOW',(0,row),(-1,row), 1, '#444444'])
            ledger_style.append(['LEFTPADDING',(0,row),(-1,row), 12])
            ledger_style.append(['FONT',(0,row),(-1,row), 'Courier-Bold'])
            group_start = (0, row+1)

            for line in entries:
                ledger_data.append([line.description, "{:,}".format(line.cost)])

                if line.cost < 0:
                    row = len(ledger_data)-1
                    ledger_style.append(['TEXTCOLOR',(1,row),(1,row), '#884444'])

            subtotal = entries.aggregate(models.Sum('cost'))['cost__sum']
            ledger_data.append(['Subtotal', "{:,}".format(subtotal)])

            row = len(ledger_data)-1
            ledger_style.append(['LINEABOVE',(0,row),(-1,row), 2, '#000000'])
            ledger_style.append(['LINEABOVE',(0,row),(-1,row), 1, '#FFFFFF'])
            ledger_style.append(['FONT',(0,row),(-1,row), 'Courier-Bold'])

            if subtotal < 0:
                ledger_style.append(['TEXTCOLOR',(1,row),(1,row), '#884444'])
        
            group_end = (-1, row)
            ledger_style.append(['LEFTPADDING', group_start, group_end, 18])
            ledger_style.append(['FONT', group_start, group_end, 'Courier'])
            
        ledger_data.append(['Closing Balance', "{:,}".format(self.stableweek.closing_balance())])
        row = len(ledger_data)-1

        ledger_style.append(['FONT',(0,row),(-1,row),'Courier-Bold'])
        ledger_style.append(['BACKGROUND',(0,row),(-1,row),'#CCCCCC'])
        ledger_style.append(['LINEABOVE',(0,row),(-1,row), 2, '#000000'])
        ledger_style.append(['LINEBELOW',(0,row),(-1,row),4,'#000000'])

        ledger_table = Table(ledger_data, self.col_widths)

        ledger_table.setStyle(TableStyle(ledger_style))

        story = self.story_header()
        story.append(ledger_table)
        return story


class LedgerPDFView(StableWeekMixin, PDFView):

    def get_report_name(self, *args, **kwargs):
        return '%s - Stable Ledger Week %2d' % (self.stable.stable_name, self.stableweek.week.week_number)

    def get(self, request, *args, **kwargs):
        self.doc = SolarisDocTemplate(request, pagesize=landscape(A4), report_name=self.get_report_name())

        report = LedgerReportSection(self.stableweek)

        self.doc.build(report.as_story())

        return self.doc.get_response()
