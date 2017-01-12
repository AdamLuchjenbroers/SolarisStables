from reportlab.lib.styles import ParagraphStyle

body_text = ParagraphStyle('body', fontName='Helvetica', fontSize=10, leading=14)

heading_1 = ParagraphStyle('heading1', fontName='Helvetica', fontSize=22, leading=28)
heading_2 = ParagraphStyle('heading2', fontName='Helvetica', fontSize=18, leading=22)
heading_3 = ParagraphStyle('heading3', fontName='Helvetica', fontSize=12, leading=14)

headings = [heading_1, heading_2, heading_3]

