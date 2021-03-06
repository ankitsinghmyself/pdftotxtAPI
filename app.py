import os
from flask import send_file
import re
import urllib.request
from flask import Flask, flash, request, redirect, render_template,url_for,send_from_directory
from werkzeug.utils import secure_filename
from pdfminer.pdfinterp import PDFResourceManager#, PDFPage.get_pages()
from pdfminer.converter import TextConverter
from io import StringIO
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter#process_pdf
from pdfminer.pdfpage import PDFPage
from pdfminer.layout import LAParams
import pathlib,os

# done = False
# #here is the animation
# def animate():
#     for c in itertools.cycle(['|', '/', '-', '\\']):
#         if done:
#             break
#         sys.stdout.write('\rloading ' + c)
#         sys.stdout.flush()
#         time.sleep(0.1)
#     sys.stdout.write('\rDone!     ')

# t = threading.Thread(target=animate)
# t.start()

# #long process here
# time.sleep(10)
# done = True
app = Flask(__name__)

UPLOAD_FOLDER = '/tmp'
app.secret_key = "1234"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
ALLOWED_EXTENSIONS = set(['pdf'])

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
	
@app.route('/')
def index():
	return render_template('index.html')

@app.route('/upload', methods=['GET', 'POST'])
def uploaded_file():
	if request.method == 'POST':
        # check if the post request has the file part
		if 'file' not in request.files:
			#flash('No file part')
			return redirect(url_for('index'))
		file = request.files['file']
		if file.filename == '':
			flash('No file selected for uploading')
			return redirect(url_for('index'))
		elif file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			text_file_path = filename
			rsrcmgr = PDFResourceManager()
			retstr = StringIO()
			laparams = LAParams()
			device = TextConverter(rsrcmgr, retstr, laparams=laparams)
			pdf_file = "/tmp/" + filename
			fp = open(pdf_file, 'rb')
			interpreter = PDFPageInterpreter(rsrcmgr, device)
			password = ""
			maxpages = 0
			caching = True
			pagenos=set()
			string=""
			for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password,caching=caching, check_extractable=True):
				interpreter.process_page(page)
				#fp.close()
				#device.close()
				string = retstr.getvalue()
				new_str = re.sub('[^a-zA-Z0-9\n]', ' ', string)
				#retstr.close()
			return new_str
		else:
			#flash('Allowed file types is pdf')
			return redirect(url_for('index'))
if __name__ == "__main__":
    app.run()