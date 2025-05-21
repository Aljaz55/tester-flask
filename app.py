import os
from flask import Flask, request, render_template, jsonify
from google.cloud import speech

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query')
    return f"Rezultati iskanja za: {query}"

@app.route('/speech-to-text', methods=['POST'])
def speech_to_text():
    audio_file = request.files['audio']
    audio_content = audio_file.read()
    
    client = speech.SpeechClient()
    audio = speech.RecognitionAudio(content=audio_content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="sl-SI",
    )

    response = client.recognize(config=config, audio=audio)
    
    if response.results:
        transcript = response.results[0].alternatives[0].transcript
        return jsonify({'transcript': transcript})
    return jsonify({'error': 'Ni bilo mogoče razumeti govora.'}), 400

if __name__ == '__main__':
    app.run(debug=True)