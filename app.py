from flask import Flask, render_template, request, send_file, jsonify
import os
from werkzeug.utils import secure_filename
import pandas as pd
from main import main  # Import your existing main function
from functions.expand_dicts import process_word_decision  # Add this import

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
            # Create data directory if it doesn't exist
            os.makedirs('data', exist_ok=True)
            
            # Run main function with the uploaded file
            results_df = main(
                path=app.config['UPLOAD_FOLDER'] + '/',
                input_file=filename,
                transform_nse=False
            )
            
            # Get unique words and their counts for dictionary expansion
            words_series = pd.Series(' '.join(results_df['Answer'].fillna('')).lower().split()).value_counts()
            avg_words_df = pd.DataFrame({
                'AVG_woord': words_series.index,
                'Count': words_series.values
            })
            # Save avg_words for dictionary expansion
            avg_words_df.to_csv('data/avg_words.csv', index=False)
            
            # Drop unnecessary columns for preview
            results_df = results_df.drop(columns=['Answer', 'flagged_word_count', 'flagged_word_type', 'total_word_count', 'unknown_word_count', 'unknown_words_not_flagged'])
            
            # Get preview of results (first 10 rows)
            preview = results_df[results_df['contains_privacy']==1]
            preview = preview.head(10).fillna('').to_dict('records')
            
            return jsonify({
                'success': True,
                'preview': preview,
                'output_filename': 'SEAA_output.csv'
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

if __name__ == '__main__':
    app.run(debug=True) 