import os
import soundfile as sf

from flask import Flask, jsonify, request, render_template, Blueprint
from flask_restplus import Api, reqparse, Resource, abort

from google.cloud import speech_v1p1beta1
from google.cloud.speech_v1p1beta1 import types
from google.protobuf.json_format import MessageToJson
from werkzeug.datastructures import FileStorage

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "ML6 Application-0e9fc2df08a1.json"

app = Flask(__name__, static_url_path='/static')
blueprint = Blueprint('api', __name__, url_prefix='/api')
api = Api(blueprint, default='api')
app.register_blueprint(blueprint)
app.config['MAX_CONTENT_LENGTH'] = 64 * 1024 * 1024  # max of 64 MB
MAX_DURATION = 120  # max duration of wav in seconds
DEBUG = False


@app.context_processor
def vars():
    return {
        'linkedin': 'https://www.linkedin.com/in/fr%C3%A9d%C3%A9rique-de-baerdemaeker-6a265610b/'
    }


client = speech_v1p1beta1.SpeechClient()


@app.route('/')
def index():
    return render_template('upload.html')


parser = reqparse.RequestParser()
parser.add_argument('file', type=FileStorage, location='files', required=True, help='.wav file to transcribe')
parser.add_argument('language', type=str, location='form', help='language code, e.g. en-US')


@api.route('/upload/', methods=['POST'])
@api.expect(parser, validate=True)
class Upload(Resource):
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

    def transcribe_file(self, file, lang):
        wav = sf.SoundFile(file)
        if 'WAV' not in wav.format:
            abort(400, 'File was recognized as %s, not WAV' % wav.format)
        if wav.subtype != 'PCM_16':
            abort(400, 'Google only accepts 16 bit PCM encoding. File is %s' % wav.subtype_info)
        if wav.frames / wav.samplerate > MAX_DURATION:
            abort(400, 'Demo file duration is limited to %s seconds' % MAX_DURATION)

        file.seek(0)
        config = types.RecognitionConfig(
            language_code=lang,
            audio_channel_count=wav.channels
        )
        audio = types.RecognitionAudio(content=file.read())
        response = client.recognize(config, audio)
        return jsonify(MessageToJson(response))

    @api.response(200, 'JSON Response returned by Google Speech to Text API')
    def post(self):
        file = request.files.get('file', None)

        if not file:
            abort(400, 'No file provided')

        if DEBUG:
            return jsonify(self.debug_resp)

        lang = request.form.get('language', 'en-US')

        return self.transcribe_file(file, lang)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)


@api.errorhandler(Exception)
def handle_invalid_usage(error):
    return {'message': str(error)}, getattr(error, 'code', 500)
