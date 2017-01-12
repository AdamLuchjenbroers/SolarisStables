from django.views.generic import View
from django.http import HttpResponse 

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, landscape
from reportlab.platypus import FrameBreak, Spacer, Paragraph, BaseDocTemplate, Frame, PageTemplate, NextPageTemplate, PageBreak
from reportlab.lib.units import cm

from . import pdf_styles

class Heading(Paragraph):
    pass

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
    def __init__(self, id='basic', columns=1, pagesize=A4, leftMargin=(2*cm), bottomMargin=(2.1*cm), colmargin=(0.5*cm)):
        (right, top) = pagesize
        right -= leftMargin
        top -= bottomMargin

        height = top - bottomMargin
        width = (right - leftMargin)
        # Subtract out blank space between columns
        colwidth = (width - ((columns - 1) * colmargin)) / columns

        frames = []
        for col in range(columns):
            left = leftMargin + (col * (colwidth + colmargin))
            frames.append(Frame(left, bottomMargin, colwidth, height))

        PageTemplate.__init__(self, id=id, frames=frames, pagesize=pagesize)
        
    def beforeDrawPage(self, canvas, doc):
        print self.id
        (width, height) = canvas._pagesize
        canvas.setLineWidth(0.2 * cm)
        canvas.line(0.5*cm, height - (2*cm), width - (0.5*cm), height - (2*cm))
        canvas.line(0.5*cm, (2*cm), width - (0.5*cm), (2*cm))

        canvas.setFont('Helvetica', 12)
        canvas.drawString(0.5*cm, height*-(1*cm), self.id)

def report_page(canvas, doc):
    pass

class ReportSection():
    page_template = 'basic'

    def __init__(self, name, level):
        self.name = name
        self.level = level

    def story_header(self):
        return [
          NextPageTemplate(self.__class__.page_template)
        , PageBreak()
        , Heading(self.name, pdf_styles.headings[self.level])      
        , Spacer(0, 0.5*cm)
        ]

    def as_story(self):
        return self.story_header()

class ListSubsection(ReportSection):
    def __init__(self, name, level, list_data):
        self.list_data = list_data

        ReportSection.__init__(self, name, level)

    def story_header(self):
        return [ Heading(self.name, pdf_styles.headings[self.level]), Spacer(0,0.3*cm) ] 

    def as_story(self):
        story = self.story_header()
        for (item, value) in self.list_data:
            story += [Paragraph('<para><b>%s:</b> %i</para>\n' % (item, value), pdf_styles.body_text)]
       
        return story 

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

        self.addPageTemplates([
          CoverPageTemplate(title, subtitle)
        , ReportPageTemplate(id='basic', pagesize=pagesize)
        , ReportPageTemplate(id='2col', columns=2, pagesize=pagesize)
        ])

    def build(self, story, canvasmaker=canvas.Canvas,):
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
