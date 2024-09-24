import os 
import glob
import pymupdf as pym 
import mmh3

use_default_or_custom = input('Would you prefer to use the default (d) or custom (c) file path? > ')
if use_default_or_custom == 'd':
    all_files = glob.glob('/Users/spencer/Documents/email_papers_script/sample_pdfs/*.pdf')
elif use_default_or_custom == 'c':
    all_files = input('Enter the full file path. >')
else:
    print('Unrecognized input. Please try again with c or d.')
    exit(0)

index = {}
for file_path in all_files:
    doc = pym.open(file_path)
    file_size = os.stat(file_path).st_size
    pdf_id = mmh3.hash(str(file_size))

    for page in doc:
        pagenum = page.number
        text = ''
        text += page.get_text()
        text_list = text.split(' ')

        for word in text_list: 
            if not index.get(word):
                index[word] = {'pdf_id':pdf_id, 'page_id':[pagenum]}
            else:
                index[word]['pdf_id'] = pdf_id
                if not pagenum in index[word]['page_id']: index[word]['page_id'].append(pagenum)

# print(index)