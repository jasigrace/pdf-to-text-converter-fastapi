from PyPDF2.utils import PdfReadError
from fastapi import FastAPI
import PyPDF2
import os

app = FastAPI()

documents_list = [doc.split('.')[0] for doc in os.listdir('documents')]
documents_extension = [doc.split('.')[1] for doc in os.listdir('documents')]


@app.get('/')
def home():
    """
    Displays all the routes available
    """
    return {"routes": ["/get_doc_list", "/parse/{doc_name}"]}


@app.get('/get_doc_list')
def get_doc_list():
    """
    Displays the list of all the documents.
    """
    return {"documents": documents_list}


@app.get('/parse/{doc_name}')
def get_doc(doc_name):
    """
    Prints the content of pdf in text format.
    """
    if doc_name in documents_list:
        doc_format = documents_extension[documents_list.index(doc_name)]
        try:
            pdf_reader = PyPDF2.PdfFileReader(f'documents/{doc_name}.{doc_format}')

        except PdfReadError:
            if doc_format != "pdf":
                return {"Error": f"Sorry, the file is not in pdf format instead in {doc_format} format."}
            else:
                return {"Error": "The Pdf File was empty"}
        else:
            txt = ""
            for i in range(pdf_reader.numPages):
                page_object = pdf_reader.getPage(i)
                txt += page_object.extractText()
            if txt:
                return txt
            else:
                return {"Error": "Sorry, the file is not readable."}
    else:
        return {"Not Found": "File not found."}
