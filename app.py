import os
from flask import Flask, jsonify, request, render_template, Response

from google.cloud import speech
from google.cloud.speech import types

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "ML6 Application-0e9fc2df08a1.json"

app = Flask(__name__)
client = speech.SpeechClient()


@app.route('/')
def index():
    return render_template('upload.html')


@app.route('/upload', methods=['POST'])
def process_wav():
    file = request.files.get('file', None)
    if not file:
        return jsonify({"error": "No file"})

    config = types.RecognitionConfig(language_code='en-US', audio_channel_count=2)
    try:
        response = client.recognize(config, types.RecognitionAudio(content=file.read()))
        return Response(str(response.results))
    except Exception as e:
        return jsonify({"error": str(e)})


if __name__ == "__main__":
    app.run()
