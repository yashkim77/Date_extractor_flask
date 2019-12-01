from flask import Flask, render_template, request,redirect,jsonify
from utility import date_extractor
import base64
from werkzeug.utils import secure_filename
import os

UPLOAD_FOLDER = 'static/'


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config["ALLOWED_EXTENSIONS"] = ["txt"]

def allowed_file(filename):
    if not "." in filename:
        return False
    ext = filename.rsplit(".", 1)[1]
    if ext in app.config["ALLOWED_EXTENSIONS"]:
        return True
    else:
        return False

@app.route('/')
def index():
	return render_template('index.html') 

@app.route('/extract_date', methods=['POST'])
def extract_date():
    if 'file1' not in request.files:
        print('No file selected')
        return redirect(request.url)
    file1 = request.files['file1']
    print(type(file1.filename))
    # if user does not select file, browser also
    # submit an empty part without filename
    if file1.filename == '':
        print('No selected file')
        return redirect(request.url)
    print(allowed_file(file1.filename))
    if file1 and allowed_file(file1.filename):
        file1.save(os.path.join(app.config["UPLOAD_FOLDER"], file1.filename))
        fh = open("01.jpeg", "wb")
        fr = open('static/'+file1.filename,"r")
        decoded = base64.b64decode(fr.read())
        fh.write(decoded)
        fh.close()
        fr.close()
        date = date_extractor('01.jpeg')
                    
    return "Date:{}".format(date)

if __name__ == '__main__':
    app.run()