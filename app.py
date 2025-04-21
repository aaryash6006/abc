from flask import Flask, render_template, request, send_from_directory, url_for
from werkzeug.utils import secure_filename
from flask_httpauth import HTTPBasicAuth
import os
from datetime import datetime

app = Flask(__name__)
auth = HTTPBasicAuth()

# Set folders
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['STATIC_FOLDER'] = 'static'

# Basic Auth for admin
users = {
    "aaryash": "strongPassword123"  # <- set your own password here
}

@auth.get_password
def get_pw(username):
    return users.get(username)

# Routes
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/blog')
def blog():
    return render_template('blog.html')

@app.route('/projects')
def projects():
    return render_template('projects.html')

@app.route('/papers')
def papers():
    return render_template('papers.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/login')
@auth.login_required
def login():
    return render_template('login.html')

@app.route('/upload', methods=['POST'])
@auth.login_required
def upload_file():
    if 'file' not in request.files:
        return "No file part"
    file = request.files['file']
    folder = request.form.get('folder', 'misc')
    if file.filename == '':
        return "No selected file"
    filename = datetime.now().strftime('%Y%m%d%H%M%S_') + secure_filename(file.filename)
    save_path = os.path.join(app.config['UPLOAD_FOLDER'], folder)
    os.makedirs(save_path, exist_ok=True)
    file.save(os.path.join(save_path, filename))
    return f"File uploaded to /uploads/{folder}/{filename}"

@app.route('/uploads/<path:filename>')
def uploaded_file(filename):
    return send_from_directory('uploads', filename)

if __name__ == '__main__':
    app.run(debug=True)

@app.route('/dashboard')
@auth.login_required
def dashboard():
    return render_template('dashboard.html')
