from django.views.generic import View
from django.http import HttpResponse 

from reportlab.pdfgen import canvas

class PDFView(View):
    def get(self, request, *args, **kwargs):
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename=\"%s\"' % self.get_pdf_name(*args, **kwargs)

        self.render_pdf(canvas.Canvas(response))
        
        return response

    def get_pdf_name(self, *args, **kwargs):
        return 'Test View.pdf'

    def render_pdf(self, canvas, *args, **kwargs):
        return canvas
