from reportlab.platypus import Table, TableStyle, KeepTogether,Spacer
from reportlab.platypus.flowables import Flowable
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.units import cm

from solaris.pdf import PDFView, ReportSection, ReportSubSection
from solaris.stablemanager.views import StableWeekMixin

from .models import RepairBill

class RepairBillSubSection(ReportSubSection):
    def __init__(self, bill, name_format='Repair Bill - %s %s', cored_format='Insurance Payout - %s %s', level=0, **kwargs):
        if bill.cored:
            name = cored_format % (bill.mech.mech_name, bill.mech.mech_code)
        else:
            name = name_format % (bill.mech.mech_name, bill.mech.mech_code)

        self.bill = bill

        ReportSubSection.__init__(self, name, level) 

    def render_queryset(self, qset, has_qty=True, has_tons=True):
        result = []

        for item in qset:
            if has_tons:
                tons = item.tons
            else:
                tons = None

            if has_qty:
                qty = item.count
            else:
                qty = None

            result.append([item.description(), qty, tons, "{:,}".format(item.cost)])
        return result

    def render_header(self, header_text, has_qty, has_tons):
        header = [header_text, None, None, 'Cost']

        if has_qty:
            header[1] = 'Qty'

        if has_tons:
            header[2] = 'Tons'

        return header

    def as_story(self):
        story = self.story_header()

        bill_data = []
        bill_style = [
          ['ALIGN', (-3,0), (-1,-1), 'RIGHT']
        ]

        lines = self.bill.lineitems
        groups = (
          ('Construction Costs', lines.construction_lines(), True, True, lines.construction_total())
        , ('Equipment Costs', lines.equipment_lines(), True, False, lines.equipment_total())
        , ('Ammunition Costs', lines.ammo_lines(), True, True, lines.ammo_total())
        , ('Labour Costs', lines.labour_lines(), False, False, None)
        )

        if self.bill.cored:
            bill_data = [
              ('Insurance', None, None, 'Payout')
            , ('Insurance Payout', None, None, self.bill.insurance_payout())
            ]

            bill_style.append(['BACKGROUND',(0,0),(-1,0), '#AAAAAA'])
            bill_style.append(['LINEBELOW',(0,0),(-1,0),1 , '#222222', 0])
            bill_style.append(['FONT',(0,0),(-1,0), 'Helvetica-Bold'])
            bill_style.append(['FONT',(-1,1),(-1,1), 'Courier-Bold'])
            bill_style.append(['LINEBELOW',(0,1),(-1,1),2 , '#222222', 0])

        else:
            for (groupname, lines, has_qty, has_tons, subtotal) in groups:
                if lines.count() < 1:
                    continue
                toprow = len(bill_data)

                bill_data.append(self.render_header(groupname, has_qty, has_tons))
                bill_style.append(['BACKGROUND',(0,toprow),(-1,toprow), '#AAAAAA'])
                bill_style.append(['FONT',(0,toprow),(-1,toprow), 'Helvetica-Bold'])
                bill_style.append(['LINEBELOW',(0,toprow),(-1,toprow),1 , '#222222'])

                bill_data += self.render_queryset(lines, has_qty=has_qty, has_tons=has_tons)
                lastrow = len(bill_data)-1
                bill_style.append(['LINEBELOW',(0,toprow+1),(-1,lastrow-1), 1 , '#666666', 0, (3,4)])
                bill_style.append(['FONT',(-1,toprow+1),(-1,lastrow), 'Courier-Bold'])

                if subtotal != None: 
                    bill_data.append(['Subtotal', None, None, "{:,}".format(subtotal)]) 

                    row = len(bill_data)-1
                    bill_style.append(['LINEABOVE',(0,row),(-1,row),1, '#222222', 0])
                    bill_style.append(['LINEBELOW',(0,row),(-1,row),1, '#222222', 0])
                    bill_style.append(['FONT',(0,row),(0,row), 'Helvetica-Bold'])
                    bill_style.append(['FONT',(-1,row),(-1,row), 'Courier-Bold'])

            bill_data.append(['Total', None, None, self.bill.lineitems.total_cost()])
            row = len(bill_data) - 1
            bill_style.append(['LINEABOVE',(0,row),(-1,row),1, '#222222', 0])
            bill_style.append(['LINEBELOW',(0,row),(-1,row),2, '#222222', 0])
            bill_style.append(['FONT',(0,row),(0,row), 'Helvetica-Bold'])
            bill_style.append(['FONT',(-1,row),(-1,row), 'Courier-Bold'])

        bill_table = Table(bill_data, [8*cm, 2*cm, 2*cm, 4*cm])
        bill_table.setStyle(TableStyle(bill_style))

        story.append(bill_table)
        return [KeepTogether(story)]

class RepairBillSection(ReportSection):
    def __init__(self, stableweek, name='Repair Costs', level=0):
        self.stableweek = stableweek
        ReportSection.__init__(self, name, level) 

    def as_story(self):
        bill_qs = RepairBill.objects.filter(stableweek__stableweek=self.stableweek, complete=True).order_by('cored')

        if bill_qs.count() < 1:
            # Don't include this section if there are no repair bills
            return []

        story = self.story_header()

        for bill in bill_qs:
            key = 'bill-%d' % bill.id
            story += RepairBillSubSection(bill, level=self.level+1, key=key).as_story()
            story.append(Spacer(0, 0.5*cm))

        return story
