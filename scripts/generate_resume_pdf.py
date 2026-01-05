from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
import textwrap

in_md = 'RESUME.md'
out_pdf = 'RESUME.pdf'

with open(in_md, 'r', encoding='utf-8') as f:
    md = f.read()

# simple plaintext conversion: remove markdown headings and links for PDF
lines = []
for line in md.splitlines():
    # remove markdown link syntax [text](url)
    import re
    line = re.sub(r"\[(.*?)\]\((.*?)\)", r"\1", line)
    # replace headings '#' with bold text markers
    line = re.sub(r"^#+\s*", "", line)
    lines.append(line)

text = "\n".join(lines)

c = canvas.Canvas(out_pdf, pagesize=A4)
width, height = A4

# Register a common font
try:
    pdfmetrics.registerFont(TTFont('DejaVuSans', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'))
    fontname = 'DejaVuSans'
except Exception:
    fontname = 'Helvetica'

c.setFont(fontname, 12)
margin = 20 * mm
usable_width = width - margin * 2
y = height - margin

for paragraph in text.split('\n\n'):
    wrapped = textwrap.wrap(paragraph, width=95)
    for wl in wrapped:
        y -= 14
        if y < margin:
            c.showPage()
            c.setFont(fontname, 12)
            y = height - margin
        c.drawString(margin, y, wl)
    y -= 8

c.save()
print('Wrote', out_pdf)
