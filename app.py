from flask import Flask, render_template, request, send_file, jsonify, Response
import os
from werkzeug.utils import secure_filename
import pandas as pd
from src.expand_dicts import process_word_decision
from queue import Queue
import json
import threading
import time
from main import main

app = Flask(__name__)

# Configure upload folder
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'output'
ALLOWED_EXTENSIONS = {'csv'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER

# Create folders if they don't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Add at app initialization
app.progress_queue = Queue()

# Global progress variable
progress = {
    "preparation": 0,
    "translation": 0,
    "processing": 0,
    "current_phase": "idle"
}

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
            # Create data directory if it doesn't exist
            os.makedirs('data', exist_ok=True)
            
            # Reset progress
            global progress
            progress = {
                "preparation": 0,
                "translation": 0,
                "processing": 0,
                "current_phase": "preparation"
            }
            
            # Define a callback function to update progress
            def update_progress(percentage, phase):
                global progress
                progress[phase] = percentage
                progress["current_phase"] = phase
                # Add more detailed debugging
                print(f"Progress update: {phase} - {percentage}% at {time.strftime('%H:%M:%S')}")
            
            # Run main function with the uploaded file and progress callback
            df = main(
                path=app.config['UPLOAD_FOLDER'] + '/',
                input_file=filename,
                progress_callback=update_progress
            )
            results_df = df[0]
            avg_words_df = df[1]

            # Save avg_words for dictionary expansion
            avg_words_df.to_csv('data/avg_words.csv', index=False)
            
            # Ensure 'flagged_word_type' column exists before dropping
            if 'flagged_word_type' not in results_df.columns:
                results_df['flagged_word_type'] = None
            
            # Drop unnecessary columns for preview
            results_df = results_df.drop(columns=[
                'Answer', 'answer_clean', 'flagged_word_count', 
                'flagged_word_type', 'total_word_count', 
                'unknown_word_count', 'unknown_words_not_flagged'
            ])
            
            # Get preview of results (first 10 rows)
            preview = results_df[results_df['contains_privacy']==1]
            preview = preview.head(10).fillna('').to_dict('records')
            
            # Get the output filename from the request form
            output_filename = request.form.get('output_filename', 'SEAA_output.csv')
            
            # Save the results to the output folder
            output_filepath = os.path.join(app.config['OUTPUT_FOLDER'], output_filename)
            results_df.to_csv(output_filepath, index=False)
            
            return jsonify({
                'success': True,
                'preview': preview,
                'output_filename': output_filename
            })
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    return jsonify({'error': 'Invalid file type'}), 400

def delete_files_in_folder(folder_path):
    # Wait for a short period to ensure files are no longer in use
    time.sleep(1)
    for file in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file)
        try:
            # Skip .gitkeep files
            if os.path.isfile(file_path) and file != '.gitkeep':
                os.unlink(file_path)
        except Exception as e:
            print(f"Error deleting file {file_path}: {e}")

@app.route('/download/<filename>')
def download_file(filename):
    try:
        # Send the file for download
        response = send_file(
            os.path.join(app.config['OUTPUT_FOLDER'], filename),
            as_attachment=True,
            download_name=filename
        )
        
        # Start background threads to delete files in both folders
        threading.Thread(target=delete_files_in_folder, args=(app.config['OUTPUT_FOLDER'],)).start()
        threading.Thread(target=delete_files_in_folder, args=(app.config['UPLOAD_FOLDER'],)).start()
        
        return response
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/expand-dicts', methods=['POST'])
def expand_dictionaries():
    try:
        data = request.get_json()
        word = data.get('word')
        decision = data.get('decision')
        
        # Load current dictionaries
        whitelist_df = pd.read_csv('dict/whitelist.txt')
        blacklist_df = pd.read_csv('dict/blacklist.txt')
        
        # Process the decision
        whitelist_df, blacklist_df = process_word_decision(
            word, decision, whitelist_df, blacklist_df
        )
        
        # Save updated dictionaries
        whitelist_df.to_csv('dict/whitelist.txt', index=False)
        blacklist_df.to_csv('dict/blacklist.txt', index=False)
        
        # Remove the processed word from avg_words.csv
        avg_words_df = pd.read_csv('data/avg_words.csv')
        avg_words_df = avg_words_df[avg_words_df['AVG_woord'] != word]
        avg_words_df.to_csv('data/avg_words.csv', index=False)
        
        return jsonify({'success': True})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/get-next-word', methods=['GET'])
def get_next_word():
    try:
        # Read the current avg_words file
        avg_words_df = pd.read_csv('data/avg_words.csv')
        
        if len(avg_words_df) == 0:
            return jsonify({'complete': True})
        
        # Get the first word and its count
        next_word = avg_words_df.iloc[0]
        
        return jsonify({
            'word': next_word['AVG_woord'],
            'count': int(next_word['Count']),
            'complete': False
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/progress')
def progress_stream():
    def generate():
        global progress
        while True:
            # Send the current progress
            data = json.dumps(progress)
            yield f"data: {data}\n\n"
            time.sleep(0.5)
            
            # If processing is complete, end the stream
            if progress["current_phase"] == "processing" and progress["processing"] >= 100:
                break
    
    return Response(generate(), mimetype='text/event-stream')

@app.route('/seaa')
def seaa():
    return render_template('seaa.html')

if __name__ == '__main__':
    app.run(debug=True) 