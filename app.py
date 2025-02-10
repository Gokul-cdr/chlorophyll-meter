from flask import Flask, render_template, request, redirect, url_for
import os
from processing import process_image  # Import image processing function

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure upload directory exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def index():
    """Renders the image upload page."""
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    """Handles image upload, processes it, and returns results."""
    if 'file' not in request.files:
        return redirect(request.url)

    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)

    if file:
        filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filename)

        # Process image for grading and identification
        plant_name, grade, chlorophyll_level, green_percentage = process_image(filename)

        return render_template('result.html', filename=file.filename, plant=plant_name,
                               grade=grade, chlorophyll=chlorophyll_level, green=green_percentage)

if __name__ == '__main__':
    app.run(debug=True)
