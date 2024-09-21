import glob 
import pymupdf as pym 

def extract_text_from_pdf(file_path):
    with pym.open(file_path) as doc:
        text = ""
        for page in doc:
            text += page.get_text()

def index_text(json_index):
    pass 