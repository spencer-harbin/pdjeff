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
        pdf_id = mmh3.hash(str(file_size) + str(os.path.getmtime(file_path)))

        file_name = file_path.split('/')[-1]

        for page in doc:
            pagenum = page.number
            text = page.get_text()

            # remove punctuation and special characters
            cleaned_text = re.sub(r'[^\w\s]', '', text)
            cleaned_text = cleaned_text.replace("\n", " ")
            text_list = cleaned_text.split()

            for word in text_list: 
                word = word.lower().strip()
                if word == '':
                    continue

                if not word in index:
                    index[word] = []

                found = False                 
                # check if PDF ID has already been recorded for current word
                for entry in index[word]:
                    if entry['pdf_id'] == pdf_id:
                        found = True
                        # if page num isn't in list already, then add it in 
                        if pagenum not in entry['page_nums']:
                            entry['page_nums'].append(pagenum)
                            break
                if not found:
                    # if the pdf ID isn't found, make a new dictionary entry 
                    index[word].append({
                        'pdf_id': pdf_id, 
                        'file_name': file_name, 
                        'page_nums': [pagenum]
                    })

    # remove duplicate page_nums
    for word in index:
        for entry in index[word]:
            entry['page_nums'] = sorted(list(set(entry['page_nums'])))

    with open('output.txt', 'w') as f:
        f.write(str(index))

    return index

def search_index(query, index):
    query = query.lower()
    if query in index:
        results = index[query]
        for result in results:
            f_name = result['file_name']
            f_id = result['pdf_id']
            f_nums = ', '.join(map(str, result['page_nums']))

            print(f'Found {query} in file {f_name} (id {f_id}) on these pages: {f_nums}')
        # print(f'Found "{query}" in file {result["pdf_filepath"]} on pages {result["page_id"]}')
    else:
        print(f'"{query}" was not found in any of the documents. If you have recently added a document, try re-creating the index.')