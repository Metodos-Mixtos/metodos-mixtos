#Se importan los paquetes necesarios
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter #process_pdf
from pdfminer.pdfpage import PDFPage
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from io import StringIO
import pandas as pd
import PyPDF2
from PyPDF2 import PdfFileReader, PdfFileWriter
from fpdf import FPDF
import tempfile

# Extraer el texto de un PDF

def pdf_to_text(pdf_name): 
    """
    Returns a string extracted from text in a PDF document.
    
    Parameters: 
        pdf_name (str): str, bytes, PDF file, path object, or file-like object. Any valid string path is acceptable. Valid
    
    """
    # PDFMiner boilerplate
    rsrcmgr = PDFResourceManager()
    sio = StringIO()
    laparams = LAParams()
    device = TextConverter(rsrcmgr, sio, laparams=laparams)
    interpreter = PDFPageInterpreter(rsrcmgr, device)

    # Extract text
    with open(pdf_name, mode='rb') as fp:
        for page in PDFPage.get_pages(fp):
            interpreter.process_page(page)

    # Get text from StringIO
    text = sio.getvalue()

    # Cleanup
    device.close()
    sio.close()

    return text

#Reportar las páginas de un pdf en las que está una palabra

def buscar_palabra(palabra, paginas):
    """
    Retorna una lista con el número de las páginas en donde está la palabra. 
    
    Parametros:
        palabra (str): la palabra que está buscando en el texto.  
        paginas (lista): Lista con las paginas del texto.  
        
    """
    matches = []
    
    for i in paginas:
        if palabra.lower().strip() in i.lower():
            posicion = paginas.index(i)
            matches.append(posicion)

    return matches

#Diccionario con las páginas en las que aparece cada una de las palabras

def diccionario_resultados(ruta, palabras):
    documento = pdf_to_text(ruta)
    paginas = documento.split('\x0c') #Split pdf text in different pages. 
    resultados = {}
    for i in palabras:
        matches = buscar_palabra(i, paginas)
        resultados[i] = matches
    return resultados

#Se crea una página en pdf con la palabra en questión

def create_pdf_with_word(text):
    pdf = FPDF()

    # Add a page
    pdf.add_page()

    # set style and size of font
    # that you want in the pdf
    pdf.set_font("Arial", size = 15)

    # create a cell
    pdf.cell(200, 75, txt = text,
             ln = 1, align = 'C')

    # save the pdf with name .pdf
    
    tempdir = tempfile.mkdtemp(prefix="pdfs_filtering-")
    r = tempdir+'/'+text+'.pdf'
    pdf.output(r) 
    
    return r

#Retorna el pdf recortado y con páginas intercaldas para indicar la palabra

def filtrar_paginas(ruta, ruta_salida, resultados, palabras):
    
    """
    Retorna el pdf recortado segun la lista de páginas. Cada página en la lista +/- una página. 
    
    Parámetros: 
        pdf: ruta al archivo. str, bytes, PDF file, path object, or file-like object. Any valid string path is acceptable.
        resultados: diccionario con la lista de palabaras y la lista de las páginas que se quiere extraer. 
        
    """
    
    file_reader = PdfFileReader(ruta)
    file_writer = PdfFileWriter()
    
    for i in palabras:
        
        palabra = create_pdf_with_word(i)
        
        pag_palabra = PdfFileReader(palabra)
        
        pag_palabra = pag_palabra.getPage(0)
        
        file_writer.add_page(pag_palabra)
        
        paginas = resultados[i]
        
        for i in paginas:
            try:
                page2 = file_reader.getPage(i-1)
                file_writer.add_page(page2)
            except:
                print('Palabra ubicada en la primera página')
            
            page1 = file_reader.getPage(i)
            file_writer.add_page(page1)
            try:
                page3 = file_reader.getPage(i+1)
                file_writer.add_page(page3)
            except:
                print('Palabra ubicada en la última página')
    
    with open(ruta_salida, mode='wb') as out:
    
        file_writer.write(out)


#Wrapper        
        
def filtrar_pdf(ruta, palabras, ruta_salida):
    
    resultados = diccionario_resultados(ruta, palabras)
    filtrar_paginas(ruta, ruta_salida, resultados, palabras)

   