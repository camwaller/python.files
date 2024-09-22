from flask import Flask, request, render_template, redirect, url_for, flash
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Configure the folder where uploaded files will be stored
UPLOAD_FOLDER = os.path.join(os.path.expanduser('~'), 'Desktop', 'python.files/uploads/')
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'mp4', 'mov'}

# User credentials
USERNAME = 'acid615'
PASSWORD = 'Cameron615'

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def check_storage_limit():
    total_size = sum(os.path.getsize(os.path.join(UPLOAD_FOLDER, f)) for f in os.listdir(UPLOAD_FOLDER) if os.path.isfile(os.path.join(UPLOAD_FOLDER, f)))
    return total_size < 250 * 1024 * 1024 * 1024  # 250 GB in bytes

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username != USERNAME or password != PASSWORD:
            flash('Invalid username or password')
            return redirect(request.url)

        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        
        if file and allowed_file(file.filename):
            if check_storage_limit():
                filename = file.filename
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                flash('File uploaded successfully')
            else:
                flash('Storage limit exceeded (250 GB). Please delete some files.')
            return redirect(request.url)

    return render_template('upload.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)