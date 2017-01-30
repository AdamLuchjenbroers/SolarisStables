from django.views.generic import View
from django.http import HttpResponse 

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, landscape
from reportlab.platypus import FrameBreak, Spacer, Paragraph, BaseDocTemplate, Frame, PageTemplate, NextPageTemplate, PageBreak
from reportlab.lib.units import cm

from PIL import Image

from . import pdf_styles

def rounded_rect(canvas, width, height, rx, x=0, y=0, kappa=0.55):
    canvas.line(x+rx, y, x+width-rx, y)
    canvas.line(x+rx, y+height, x+width-rx, y+height)
    canvas.line(x, y+height-rx, x, y+rx)
    canvas.line(x+width, y+height-rx, x+width, y+rx)

    kx = rx * kappa

    canvas.bezier(x+rx,y, x+rx-kx,y, x,y+rx-kx, x,y+rx)
    canvas.bezier(x+width-rx,y, x+width-rx+kx,y, x+width,y+rx-kx, x+width,y+rx)
    canvas.bezier(x+rx,y+height, x+rx-kx,y+height, x,y+height-rx+kx, x,y+height-rx)
    canvas.bezier(x+width-rx,y+height, x+width-rx+kx,y+height, x+width,y+height-rx+kx, x+width,y+height-rx)

def rounded_square(canvas, size, rx, **kwargs):
    rounded_rect(canvas, size, size, rx, **kwargs)

class Heading(Paragraph):
    def __init__(self, *args, **kwargs):
        self.level = kwargs.get('level', 0)
        self.full_page = kwargs.get('full_page', False)
        self.key = kwargs.get('key', None)
        self.closed = kwargs.get('closed', False)

        Paragraph.__init__(self, *args)

    def draw(self, *args, **kwargs):
        if self.key != None:
            if self.full_page:
                self.canv.bookmarkPage(self.key)
            else:
                self.canv.bookmarkHorizontal(self.key, 0, 2*cm)

            self.canv.addOutlineEntry(self.getPlainText(), self.key, self.level, self.closed)

        Paragraph.draw(self, *args, **kwargs)

class SolarisPageTemplate(PageTemplate):
    def beforeDrawPage(self, canvas, doc):
        if self.background != None:
            self.background.draw_on(canvas)

        (width, height) = canvas._pagesize
        canvas.setLineWidth(0.2 * cm)
        canvas.line(cm, height - (2*cm), width - cm, height - (2*cm))
        canvas.line(cm, (2*cm), width - cm, (2*cm))

class CoverPageTemplate(SolarisPageTemplate):
    def __init__(self, title, subtitle, background=None):
        self.title = title
        self.subtitle = subtitle
        self.background = background
        
        dummy = Frame(1, 1, 200, 200, id='dummy')
        #ReportLab uses old style classes, so super() doesn't work.
        PageTemplate.__init__(self, id='cover', frames=[dummy])

    def beforeDrawPage(self, canvas, doc):
        SolarisPageTemplate.beforeDrawPage(self, canvas, doc)

        (width, height) = canvas._pagesize

        if self.title != None:
            canvas.setFont('Helvetica', 64)
            canvas.drawString(1.5*cm, height*0.5, self.title)
    
        if self.subtitle != None:
            canvas.setFont('Helvetica', 32)
            canvas.drawString(1.5*cm, (height*0.5)-(3*cm), self.subtitle)

class ReportPageTemplate(SolarisPageTemplate):
    def __init__(self, id='basic', columns=1, pagesize=A4, leftMargin=(2*cm), bottomMargin=(2.1*cm), colmargin=(0.5*cm), background=None):
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

        self.background = background
        PageTemplate.__init__(self, id=id, frames=frames, pagesize=pagesize)

def report_page(canvas, doc):
    pass

class ReportSection():
    page_template = 'basic'

    def __init__(self, name, level, key=None, closed=False):
        self.name = name
        self.level = level
        self.closed = closed

        if key == None:
            # If no key is provided, use a crude override
            key = name.replace(' ','-').lower()
        self.key = key

    def story_header(self):
        return [
          NextPageTemplate(self.__class__.page_template)
        , PageBreak()
        , Heading(self.name, pdf_styles.headings[self.level], key=self.key, level=self.level, closed=self.closed, full_page=True)      
        , Spacer(0, 0.5*cm)
        ]

    def as_story(self):
        return self.story_header()

class ReportSubSection(ReportSection):
    def __init__(self, name, level, **kwargs):
        self.key = kwargs.get('key', name.replace(' ','-').lower())
        ReportSection.__init__(self, name, level, **kwargs)

    def story_header(self):
        return [ 
          Heading(self.name, pdf_styles.headings[self.level], key=self.key, level=self.level, closed=True) 
        , Spacer(0,0.3*cm)
        ] 

class ListSubsection(ReportSubSection):
    def __init__(self, name, level, list_data):
        self.list_data = list_data

        ReportSubSection.__init__(self, name, level)

    def as_story(self):
        story = self.story_header()
        for (item, value) in self.list_data:
            story += [Paragraph('<para><b>%s:</b> %i</para>\n' % (item, value), pdf_styles.body_text)]
       
        return story 

class BackgroundImage():
    def __init__(self, bg_image, pagesize, base_fade=0.25, footer_size=(1.9*cm), header_size=(1.9*cm)):
        body_width = pagesize[0]
        body_height = pagesize[1] - (footer_size + header_size) 

        self.image = Image.open(bg_image).convert('L')

        (im_width, im_height) = self.image.size

        resize = body_height / im_height
        self.draw_width = im_width * resize

        if self.draw_width <= body_width:
            self.draw_x = 0
            draw_fade = True
        else:
            self.draw_x = ((im_width * resize) - body_width) / 2
            draw_fade = False

        # Apply a consistent fade to the whole image, feathering the left edge if
        # required
        im_data = self.image.load()
        for x in range(im_width):
            for y in range(im_height):
                lum = im_data[x,y]

                if x >= im_width - 200 and draw_fade:
                    fade = base_fade * ((im_width - x) / 200.0)
                else:
                    fade = base_fade

                new_lum = 255 - int(((255 - lum) * fade))
                im_data[x,y] = new_lum

        self.draw_y = footer_size
        self.draw_height = body_height

    def draw_on(self, canvas):
        canvas.drawInlineImage(self.image, self.draw_x, self.draw_y, self.draw_width, self.draw_height)


class SolarisDocTemplate(BaseDocTemplate):
    def __init__(self, request, report_name="Test PDF", title="Test PDF", subtitle=None, pagesize=A4, background=None, **kwargs):
        self.request = request
        self.report_name = report_name
        self.title = title
        self.subtitle = subtitle

        self.response = HttpResponse(content_type='application/pdf')
        self.response['Content-Disposition'] = 'attachment; filename=\"%s.pdf\"' % self.report_name

        #ReportLab uses old style classes, so super() doesn't work.
        BaseDocTemplate.__init__(self, self.response, pagesize=pagesize, **kwargs)

        if background != None:
            bg_image = BackgroundImage(background, pagesize)
        else: 
            bg_image = None

        self.addPageTemplates([
          CoverPageTemplate(title, subtitle, background=bg_image)
        , ReportPageTemplate(id='basic', pagesize=pagesize, background=bg_image)
        , ReportPageTemplate(id='2col', columns=2, pagesize=pagesize, background=bg_image)
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
