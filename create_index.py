import pymupdf as pym 
import os
import mmh3
import re

def create_index(all_files):
    # add logic later to check if an index already exists 
    index = {}
    for file_path in all_files:
        doc = pym.open(file_path)
        file_size = os.stat(file_path).st_size
        pdf_id = mmh3.hash(str(file_size))

        for page in doc:
            pagenum = page.number
            text = ''
            text += page.get_text()

            # remove punctuation and special characters
            cleaned_text = re.sub(r'[^\w\s]', '', text)
            cleaned_text = cleaned_text.replace("\n", " ")
            text_list = cleaned_text.split(' ')

            for word in text_list: 
                word = word.lower()
                if not index.get(word):
                    index[word] = {'pdf_ids':[pdf_id], 'pdf_filepaths':[file_path], 'page_ids':[pagenum]}
                else:
                    index[word]['pdf_ids'].append(pdf_id)
                    index[word]['pdf_filepaths'].append(file_path)
                    if not pagenum in index[word]['page_ids']: index[word]['page_ids'].append(pagenum)

    return index

def search_index(query, index):
    query = query.lower()
    if query in index:
        result = index[query]
        print(f'Found "{query}" in file {result["pdf_filepath"]} on pages {result["page_id"]}')
    else:
        print(f'"{query}" was not found in any of the documents. If you have recently added a document, try re-creating the index.')