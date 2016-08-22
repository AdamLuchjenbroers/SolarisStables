from solaris.pdf import PDFView
from .views import StableWeekMixin

class StablePDFReport(StableWeekMixin, PDFView):
    def get_pdf_name(self, *args, **kwargs):
        return 'Test View.pdf'

    def render_pdf(self, canvas, *args, **kwargs):
