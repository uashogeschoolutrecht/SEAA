from flask import Flask, render_template, request, send_file, jsonify
import os
from werkzeug.utils import secure_filename
import pandas as pd
from main import main  # Import your existing main function

app = Flask(__name__)

# Configure upload folder
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'outputs'
ALLOWED_EXTENSIONS = {'csv'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER

# Create folders if they don't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        try:
            # Run main function with the uploaded file
            results_df = main(
                path=app.config['OUTPUT_FOLDER'] + '/',
                input_file=filename,
                transform_nse=False
            )
            
            # Save results
            output_filename = 'SEAA_output.csv'
            output_path = os.path.join(app.config['OUTPUT_FOLDER'], output_filename)
            results_df.to_csv(output_path, sep=';', encoding='utf-8-sig')
            
            # Get preview of results
            preview = results_df.head().to_dict('records')
            
            return jsonify({
                'success': True,
                'preview': preview,
                'output_filename': output_filename
            })
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    return jsonify({'error': 'Invalid file type'}), 400

@app.route('/download/<filename>')
def download_file(filename):
    try:
        return send_file(
            os.path.join(app.config['OUTPUT_FOLDER'], filename),
            as_attachment=True,
            download_name=filename
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True) 