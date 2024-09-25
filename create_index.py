import pymupdf as pym 
import os
import mmh3
import re
import sqlite3 

# will create a database if it doesn't already exist
conn = sqlite3.connect('pdf_index.db')
cursor = conn.cursor()

# creates tables if they don't exist (again)
cursor.execute('''CREATE TABLE IF NOT EXISTS pdfs (
               pdf_id INTEGER PRIMARY KEY, 
               file_name TEXT, 
               file_size INTEGER, 
               last_modified INTEGER
               )''')

cursor.execute('''CREATE TABLE IF NOT EXISTS index(
               word TEXT, 
               pdf_id INTEGER, 
               page_num INTEGER, 
               FOREIGN KEY(pdf_id) REFERENCES pdfs(pdf_id)
               )''')

# insert pdf metadata into pdfs table
def insert_pdf(pdf_id, file_name, file_size, last_modified):
    cursor.execute('''INSERT OR IGNORE INTO pdfs (pdf_id, file_name, file_size, last_modified)
                    VALUES (?, ?, ?, ?)''', (pdf_id, file_name, file_size, last_modified))
    conn.commit()

# insert word occurrences into index table
def insert_index_entry(word, pdf_id, page_num):
    cursor.execute('''INSERT INTO index (word, pdf_id, page_num)
                   VALUES (?, ?, ?)''', (word, pdf_id, page_num))
    conn.commit()

def create_index(all_files):
    # add logic later to check if an index already exists 
    index = {}
    for file_path in all_files:
        doc = pym.open(file_path)
        file_size = os.stat(file_path).st_size
        pdf_id = mmh3.hash(str(file_size) + str(os.path.getmtime(file_path)))

        file_name = file_path.split('/')[-1]

        # insert pdf metadata into pdf table
        insert_pdf(pdf_id, file_name, file_size, last_modified=os.path.getmtime(file_path))

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

    pipe_dict_into_sqlite(index)

    # remove duplicate page_nums
    for word in index:
        for entry in index[word]:
            entry['page_nums'] = sorted(list(set(entry['page_nums'])))

    with open('output.txt', 'w') as f:
        f.write(str(index))

    return index

def pipe_dict_into_sqlite(index):
    for word, entries in index.items():
        for entry in entries:
            pdf_id = entry['pdf_id']
            page_nums = entry['page_nums']

            # insert each page number for the word into index table
            for page_num in page_nums:
                insert_index_entry(word, pdf_id, page_num)

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