import os
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = '/Users/spencer/Documents/email_papers_script/sample_pdfs'
ALLOWED_EXTENSIONS = {'pdf', 'txt'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# only upload pdf and txt files
def allowed_file(filename):
    return '.' and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/")
def hello_world():
    return "<p>Hello, world!</p>"

@app.route("/test")
def test_route():
    return "<p>this is a test route</p>"

@app.route("/upload_pdf", methods=['GET', 'POST'])
def upload_pdf():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        
        # file = request.files['file']
        files = request.files.getlist('file')

        for file in files:
            if file.filename == '':
                flash('No file selected')
                return redirect(request.url)
            
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                return redirect(url_for('download_file', name=filename))
        
    return '''
    <!doctype html>
    <title>Upload new file</title>
    <h1>Upload new file</h1>
    <form method=post enctype=multipart/form-data>
        <input type=file name=file multiple>
        <input type=submit value=Upload>
    </form>
    '''