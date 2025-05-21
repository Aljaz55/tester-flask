import os
from flask import Flask, request, render_template, jsonify
from google.cloud import speech

# Initialize Flask app
app = Flask(__name__)

# Route to render the search form with voice input
@app.route('/')
def index():
    return render_template('index.html')

# Route to handle the search query
@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query')  # Get the query from the search bar
    # You can add more logic here to process the query (e.g., search in a database)
    return f"Rezultati iskanja za: {query}"

# Route to handle the speech-to-text request
@app.route('/speech-to-text', methods=['POST'])
def speech_to_text():
    # Get the audio file from the frontend
    audio_file = request.files['audio']

    # Convert the audio file to bytes
    audio_content = audio_file.read()

    # Initialize Google Cloud Speech client
    client = speech.SpeechClient()

    # Prepare the audio for recognition
    audio = speech.RecognitionAudio(content=audio_content)

    # Set up the configuration for speech recognition (Slovenian)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="sl-SI",  # Slovenian language code
    )

    # Recognize speech
    response = client.recognize(config=config, audio=audio)

    # Extract the transcribed text from the response
    if response.results:
        transcript = response.results[0].alternatives[0].transcript
        return jsonify({'transcript': transcript})
    else:
        return jsonify({'error': 'Ni bilo mogoče razumeti govora.'}), 400

if __name__ == '__main__':
    app.run(debug=True)