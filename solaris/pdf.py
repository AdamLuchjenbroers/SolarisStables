from django.views.generic import View
from django.http import HttpResponse 

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, landscape
from reportlab.platypus import BaseDocTemplate, Frame, PageTemplate, NextPageTemplate, PageBreak
from reportlab.lib.units import cm

class CoverPageTemplate(PageTemplate):
    def __init__(self, title, subtitle):
        self.title = title
        self.subtitle = subtitle
        
        dummy = Frame(1, 1, 200, 200, id='dummy')
        #ReportLab uses old style classes, so super() doesn't work.
        PageTemplate.__init__(self, id='cover', frames=[dummy])

    def beforeDrawPage(self, canvas, doc):
        (width, height) = canvas._pagesize

        if self.title != None:
            canvas.setFont('Helvetica', 64)
            canvas.drawString(1.5*cm, height*0.5, self.title)
    
        if self.subtitle != None:
            canvas.setFont('Helvetica', 32)
            canvas.drawString(1.5*cm, (height*0.5)-(3*cm), self.subtitle)
    
        canvas.setLineWidth(0.2 * cm)
        canvas.line(0.5*cm, height - (2*cm), width - (0.5*cm), height - (2*cm))
        canvas.line(0.5*cm, (2*cm), width - (0.5*cm), (2*cm))

class ReportPageTemplate(PageTemplate):
    def __init__(self, id='basic', columns=1, pagesize=A4, leftMargin=(2*cm), bottomMargin=(0.5*cm), colmargin=(0.5*cm)):
        (left, bottom) = (leftMargin, bottomMargin)
        (right, top) = pagesize
        right -= leftMargin
        top -= bottomMargin

        height = top - bottom
        width = (right - left)
        # Subtract out blank space between columns
        colwidth = (width - ((columns - 1) * colmargin)) / columns

        frames = []
        for col in range(columns):
            left = leftMargin + (col * (colwidth + colmargin))
            frames.append(Frame(left, bottomMargin, height, colwidth, showBoundary=1))

        PageTemplate.__init__(self, id=id, frames=frames)
        
    def beforeDrawPage(self, canvas, doc):
        canvas.setLineWidth(0.2 * cm)
        canvas.line(0.5*cm, height - (2*cm), width - (0.5*cm), height - (2*cm))
        canvas.line(0.5*cm, (2*cm), width - (0.5*cm), (2*cm))

def report_page(canvas, doc):
    pass

class ReportSection():
    def __init__(self):
        pass

    def as_story(self):
        return []

class SolarisDocTemplate(BaseDocTemplate):
    def __init__(self, request, report_name="Test PDF", title="Test PDF", subtitle=None, pagesize=A4, **kwargs):
        self.request = request
        self.report_name = report_name
        self.title = title
        self.subtitle = subtitle

        self.response = HttpResponse(content_type='application/pdf')
        self.response['Content-Disposition'] = 'attachment; filename=\"%s.pdf\"' % self.report_name

        #ReportLab uses old style classes, so super() doesn't work.
        BaseDocTemplate.__init__(self, self.response, pagesize=pagesize, **kwargs)

        cover = CoverPageTemplate(title, subtitle)

        all_page = Frame(self.leftMargin, self.bottomMargin, self.width, self.height, id='body')
        self.addPageTemplates([cover, PageTemplate(id='basic',frames=[all_page]) ])

    def build(self, story, canvasmaker=canvas.Canvas):
        story.insert(0,NextPageTemplate('basic')) 

        return BaseDocTemplate.build(self, story, canvasmaker=canvasmaker)

    def __unicode__(self):
        return 'StableDocTemplate: %s (%s) -> %s' % (self.title, self.subtitle, self.filename)

    def get_response(self):
        return self.response

class PDFView(View):
    pagesize = A4 

    def get(self, request, *args, **kwargs):
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename=\"%s.pdf\"' % self.get_report_name(*args, **kwargs)

        pdf = canvas.Canvas(response, pagesize=self.__class__.pagesize)

        self.render_pdf(pdf)
        
        return response

    def get_page_dimensions(self):
        return self.__class__.pagesize

    def get_report_name(self, *args, **kwargs):
        return 'Test View.pdf'

    def render_pdf(self, pdf, *args, **kwargs):
        return pdf
