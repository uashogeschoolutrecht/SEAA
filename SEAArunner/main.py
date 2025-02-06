import pandas as pd
from functions.load_seaa_data import load_data, load_dictionary
from functions.nse.transform_raw_data import transform_nse_data
from functions.SEAA import SEAA
from langdetect import detect
from functions.AVG_list import AVG_list
from functions.expand_dicts import expand_dicts
from functions.get_medewerkers_names import get_medewerkers_names
import azure.functions as func
from flask import Flask, request, send_from_directory
import logging
import os

# Import your existing Flask app
import app

app = Flask(__name__)

# Serve the static files
@app.route('/')
def index():
    return send_from_directory('templates', 'index.html')

@app.route('/static/<path:path>')
def serve_static(path):
    return send_from_directory('static', path)

def main(req: func.HttpRequest) -> func.HttpResponse:
    """
    The main entry point for the Azure Function App.
    """
    logging.info('Python HTTP trigger function processed a request.')

    # Get the route from the request
    route = req.route_params.get('route', '')
    
    # Create the WSGI environment
    environ = {
        'wsgi.version': (1, 0),
        'wsgi.input': req.get_body(),
        'wsgi.errors': logging.getLogger(),
        'wsgi.multithread': False,
        'wsgi.multiprocess': False,
        'wsgi.run_once': False,
        'REQUEST_METHOD': req.method,
        'SCRIPT_NAME': '',
        'PATH_INFO': f'/{route}' if route else '/',
        'QUERY_STRING': req.query_string.decode(),
        'SERVER_NAME': 'localhost',
        'SERVER_PORT': '443',
        'SERVER_PROTOCOL': 'HTTP/1.1',
        'wsgi.url_scheme': 'https',
        'CONTENT_LENGTH': req.headers.get('Content-Length', ''),
        'CONTENT_TYPE': req.headers.get('Content-Type', ''),
    }

    # Add HTTP headers
    for key, value in req.headers.items():
        key = key.upper().replace('-', '_')
        if key not in ('CONTENT_TYPE', 'CONTENT_LENGTH'):
            key = f'HTTP_{key}'
        environ[key] = value

    # Create response buffer
    response_headers = []
    response_status = ['200 OK']
    response_body = []

    def start_response(status, headers):
        response_status[0] = status
        response_headers.extend(headers)

    # Get response from Flask app
    response = app.wsgi_app(environ, start_response)
    response_body.extend(response)

    # Convert response to bytes if it's not already
    body = b''.join(response_body) if isinstance(response_body[0], bytes) else ''.join(response_body).encode()

    # Convert headers to dict
    headers = {name: value for name, value in response_headers}

    return func.HttpResponse(
        body=body,
        status_code=int(response_status[0].split()[0]),
        headers=headers,
        mimetype=headers.get('Content-Type', 'text/html')
    )

def main_local(
    path, 
    input_file=None,
    transform_nse=False,
    limit=-1
):
    """
    Process and analyze open-ended survey responses, with optional NSE (National Student Survey) support.
    
    Args:
        path (str): Directory path where input/output files are stored
        input_file (str): Name of the input CSV file to process. Must contain these columns:
            - 'answer': The text responses to analyze
            - 'respondent_id': Unique identifier for each respondent
            - 'question_id': Identifier for the question being answered
        transform_nse (bool, optional): Set to True if input is a raw NSE file that needs transformation
        limit (int, optional): Limit the number of responses to process. Default -1 (process all)
    
    Required Input Format:
    The input CSV file must be semicolon-separated (;) and contain the following columns:
    - answer: The actual text responses
    - respondent_id: Unique identifier for each respondent
    - question_id: Identifier for the question being answered
    
    Output:
    - SEAA_output.csv: Main analysis results
    - avg_words_count.csv: List of unknown words for review
    - Updated whitelist.txt and blacklist.txt in the dict/ folder
    """
    
    # Handle NSE transformation if requested
    if transform_nse:
        if input_file is None:
            raise ValueError("input_file must be provided when transform_nse is True")
        transform_nse_data(
            input_path=path,
            input_file_name=input_file,
        )
        input_file = 'nse_transformed.csv'
    
    if input_file is None:
        raise ValueError("Please provide an input_file name")

    nseant_df = load_data(path, input_file)
    # Import latest employee names
    # get_medewerkers_names()

    # Import dictionaries
    word_list_df = load_dictionary(file_name="wordlist.txt", dict_type='known')
    whitelist_df = load_dictionary(file_name='whitelist.txt', dict_type='known')
    
    word_list_df = pd.concat([word_list_df, whitelist_df], ignore_index=True)

    # Flag words
    flag_df = pd.DataFrame()
    for file_name,file_type in [('illness.txt', 'illness'), ('studiebeperking.txt', 'disability'), ('names.txt', 'name'), ('blacklist.txt', 'blacklist')]:
        temp_df = load_dictionary(file_name=file_name, dict_type=file_type)
        flag_df = pd.concat([flag_df, temp_df], ignore_index=True)
    del temp_df

    result_df = SEAA(nseant_df, word_list_df, flag_df,limit=limit)
 
    # Language detection    
    def detect_language(text):
        try:
            return detect(text)
        except:
            return None

    result_df['language'] = result_df['answer_clean'].apply(detect_language)
    
    # Get all avg words that are not flagged yet
    avg_words_df = AVG_list(result_df[result_df["language"] == 'nl'].copy(),flag_df)
    avg_words_df = avg_words_df.merge(flag_df, 'left', left_on='AVG_woord', right_on='words')
    avg_words_df = avg_words_df[avg_words_df['words'].isna()].drop(columns='words')

    # Save unknown words to file
    # file_name = 'avg_words_count.csv'
    # avg_words_df.to_csv(f'{path}{file_name}', sep=';', encoding='utf-8-sig')

    # # Import blacklist
    # blacklist_df = load_dictionary(file_name='blacklist.txt', dict_type='known')

    # # Expand upon the blacklist and/or whitelist
    # whitelist_df, blacklist_df = expand_dicts(avg_words_df, whitelist_df, blacklist_df)
    
    # # Save lists to file
    # whitelist_df.to_csv(f'dict//whitelist.txt', index=False) 
    # blacklist_df.to_csv(f'dict//blacklist.txt', index=False)

    return result_df, avg_words_df

# # ALL INPUTS must be csv files
# # Set input file, if NSE transform is required define the transform_nse object, for any other input file define the input_file object
# transform_nse = None

# # Make sure that the input file has the following columns: respondent_id, Answer, question_id, in this order and with the correct headers.
# input_file = "combined_responses_100_dagen_2024_2025.csv"


# # Set path to the folder where the input and output files are stored
# path = r'C:\Users\AnneL\Stichting Hogeschool Utrecht\FCA-DA-P - Analytics\Open antwoorden\data'

# # Run the main function
# results_df = main(path, transform_nse=transform_nse, input_file=input_file)
#     # Save results to output file
# file_name = '\\SEAA_output_100_dagen_2024_2025.csv'
# results_df.to_csv(f'{path}{file_name}', sep=';', encoding='utf-8-sig')


