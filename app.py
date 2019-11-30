import os
from flask import Flask, jsonify, request, render_template

from google.cloud import speech
from google.cloud.speech import types
from google.protobuf.json_format import MessageToJson

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "ML6 Application-0e9fc2df08a1.json"

app = Flask(__name__, static_url_path='/static')


@app.context_processor
def vars():
    return {
        'linkedin': 'https://www.linkedin.com/in/fr%C3%A9d%C3%A9rique-de-baerdemaeker-6a265610b/'
    }


client = speech.SpeechClient()
debug = False
debug_resp = """
{"results": [
        {
            "alternatives": [
                {
                    "transcript": "oh yeah Vine",
                    "confidence": 0.8270418047904968
                }
            ]
        }
    ]}
"""


@app.route('/')
def index():
    return render_template('upload.html')


@app.route('/upload', methods=['POST'])
def process_wav():
    file = request.files.get('file', None)
    if not file:
        raise InvalidUsage('No file provided')

    if debug:
        return jsonify(debug_resp)

    config = types.RecognitionConfig(language_code='en-US', audio_channel_count=2)
    try:
        response = client.recognize(config, types.RecognitionAudio(content=file.read()))
        return jsonify(MessageToJson(response))
    except Exception as e:
        raise InvalidUsage(str(e))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)


class InvalidUsage(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv


@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response