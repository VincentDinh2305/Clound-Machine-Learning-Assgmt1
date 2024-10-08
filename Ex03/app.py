from chalice import Chalice
from chalicelib import storage_service, recognition_service, translation_service, text_to_speech_service
import base64
import json

#####
# chalice app configuration
#####
app = Chalice(app_name='Capabilities')
app.debug = True

#####
# services initialization
#####
storage_location = 'contents.aws.ai'
storage_service = storage_service.StorageService(storage_location)
recognition_service = recognition_service.RecognitionService(storage_service)
translation_service = translation_service.TranslationService()
text_to_speech_service = text_to_speech_service.TextToSpeechService()

#####
# RESTful endpoints
#####
@app.route('/images', methods=['POST'], cors=True)


def upload_image():
    request_data = json.loads(app.current_request.raw_body)
    file_name = request_data['filename']
    file_bytes = base64.b64decode(request_data['filebytes'])
    image_info = storage_service.upload_file(file_bytes, file_name)
    return image_info
@app.route('/images/{image_id}/translate-text', methods=['POST'], cors=True)


def translate_image_text(image_id):
    request_data = json.loads(app.current_request.raw_body)
    from_lang = request_data['fromLang']
    to_lang = request_data['toLang']

    MIN_CONFIDENCE = 80.0

    text_lines = recognition_service.detect_text(image_id)

    translated_lines = []
    for line in text_lines:
        if float(line['confidence']) >= MIN_CONFIDENCE:
            translated_line = translation_service.translate_text(line['text'], from_lang, to_lang)
            # Convert the translated text into speech
            speech_url = text_to_speech_service.convert_text_to_speech(translated_line, to_lang)
            translated_lines.append({
                'text': line['text'],
                'translation': translated_line,
                'boundingBox': line['boundingBox'],
                'speechUrl': speech_url
            })

    return translated_lines
