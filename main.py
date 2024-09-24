import pymupdf as pym 
import mmh3

file_path = '/Users/spencer/Documents/email_papers_script/sample_pdfs/test.pdf'

index = {}

doc = pym.open(file_path)

# update this later to use file size or something instead of just file path
pdf_id = mmh3.hash(file_path)

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

print(index)

# I don't want to do this today