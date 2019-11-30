import os
from flask import Flask, jsonify, request, render_template, Blueprint
from flask_restplus import Api, reqparse, Resource, abort

from google.cloud import speech
from google.cloud.speech import types
from google.protobuf.json_format import MessageToJson
from werkzeug.datastructures import FileStorage

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "ML6 Application-0e9fc2df08a1.json"

app = Flask(__name__, static_url_path='/static')
blueprint = Blueprint('api', __name__, url_prefix='/api')
api = Api(blueprint, default='api')
app.register_blueprint(blueprint)


@app.context_processor
def vars():
    return {
        'linkedin': 'https://www.linkedin.com/in/fr%C3%A9d%C3%A9rique-de-baerdemaeker-6a265610b/'
    }


client = speech.SpeechClient()
debug = False


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
        config = types.RecognitionConfig(language_code=lang, audio_channel_count=2)
        audio = types.RecognitionAudio(content=file.read())
        response = client.recognize(config, audio)
        return jsonify(MessageToJson(response))

    @api.response(200, 'JSON Response returned by Google Speech to Text API')
    def post(self):
        file = request.files.get('file', None)

        if not file:
            abort(400, 'No file provided')

        if debug:
            return jsonify(self.debug_resp)

        lang = request.form.get('language', 'en-US')

        return self.transcribe_file(file, lang)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)


@api.errorhandler(Exception)
def handle_invalid_usage(error):
    return {'message': str(error)}, getattr(error, 'code', 500)
