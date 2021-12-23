from PyPDF2 import PdfFileWriter, PdfFileReader
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from csv import DictReader
import subprocess
import shlex

sourcePDF="./comandos/justificante.pdf"

def genera_justificante(name, dni, hInit, hFin, dia, prof ):
    packet = io.BytesIO()
    # create a new PDF with alumn name
    can = canvas.Canvas(packet, pagesize=letter)
    can.drawString(290, 465, name)
    can.drawString(150, 440, dni)
    can.drawString(185, 410, hInit)
    can.drawString(270, 410, hFin)
    can.drawString(380, 410, dia)
    can.drawString(160, 360, dia)

    can.drawString(120, 295, prof)
    can.save()

    #move to the beginning of the StringIO buffer
    packet.seek(0)
    new_pdf = PdfFileReader(packet)
    # read your existing PDF
    existing_pdf = PdfFileReader(open(sourcePDF, "rb"))
    output = PdfFileWriter()
    # add the "watermark" (which is the new pdf) on the existing page
    page = existing_pdf.getPage(0)
    page.mergePage(new_pdf.getPage(0))
    output.addPage(page)
    # finally, write "output" to a real file
    outputStream = open(dni+"-"+hInit[0:hInit.index(":")]+"-"+dia[0:2]+".pdf", "wb")
    output.write(outputStream)
    outputStream.close()
    return dni+"-"+hInit[0:hInit.index(":")]+"-"+dia[0:2]+".pdf"