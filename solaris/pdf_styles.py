from reportlab.lib.styles import ParagraphStyle

body_text = ParagraphStyle('body', fontName='Helvetica', fontSize=10, leading=12)

heading_1 = ParagraphStyle('heading1', fontName='Helvetica', fontSize=16, leading=20)
heading_2 = ParagraphStyle('heading2', fontName='Helvetica', fontSize=14, leading=18)
heading_3 = ParagraphStyle('heading3', fontName='Helvetica', fontSize=12, leading=14)

headings = [heading_1, heading_2, heading_3]

