import glob 
import pymupdf as pym 

class PdfIndex:
    def __init__(self, local_file_path):
        self.local_file_path = local_file_path
        self.index = {}

    def extract_text_from_pdf(self):
        text = ""
        doc = pym.open(self.local_file_path)
        for page in doc:
            text += page.get_text()
        
        doc.close()

        return text
    
    def index_pdf_contents(self):
        pass