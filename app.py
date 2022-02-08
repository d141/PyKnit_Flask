import os
from flask import Flask, render_template, jsonify, flash, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename

import pyknit_methods as pk

UPLOAD_FOLDER = '/Users/davevananda/PycharmProjects/PyKnit_Flask/uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/')
def welcome():
    return render_template('index.html')  # render a template


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/barcodes', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        for f in request.files.getlist('file'):
            if f and allowed_file(f.filename):
                filename = secure_filename(f.filename)
                f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return render_template("barcodes.html")
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file multiple>
      <input type=submit value=Upload>
    </form>
    '''


@app.route('/uploads/<name>')
def download_file(name):
    return send_from_directory(app.config["UPLOAD_FOLDER"], name)


'''
@app.route('/barcodes')
def home():
    return render_template('barcodes.html')
'''

# start the server with the 'run()' method
if __name__ == '__main__':
    app.run(debug=True)
