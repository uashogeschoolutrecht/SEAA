import azure.functions as func
from flask import Flask, send_from_directory
import logging
import os

app = Flask(__name__)

# Import your routes and other Flask configurations
@app.route('/')
def serve_index():
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