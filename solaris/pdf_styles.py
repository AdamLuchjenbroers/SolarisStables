from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm

body_text = ParagraphStyle('body', fontName='Helvetica', fontSize=10, leading=14)
indented_text = ParagraphStyle('indented', parent=body_text, leftIndent=1.7*cm)

heading_1 = ParagraphStyle('heading1', fontName='Helvetica-Bold', fontSize=22, leading=28)
heading_2 = ParagraphStyle('heading2', fontName='Helvetica-Bold', fontSize=18, leading=22)
heading_3 = ParagraphStyle('heading3', fontName='Helvetica-Bold', fontSize=14, leading=18)

headings = [heading_1, heading_2, heading_3]

