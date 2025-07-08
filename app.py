
from flask import Flask, request, jsonify
from gtts import gTTS
from moviepy.editor import TextClip, CompositeVideoClip, AudioFileClip
import os

app = Flask(__name__)
app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return "✅ Hindi Shorts Bot is Live! Use POST /generate to submit your topic."

@app.route('/generate', methods=['POST'])
def generate_video():
    data = request.json
    text = data.get("text", "India is a country of unity in diversity.")
    lang = data.get("lang", "hi")

    try:
        tts = gTTS(text=text, lang=lang)
        tts.save("audio.mp3")
        audio = AudioFileClip("audio.mp3")

        text_clip = TextClip(text, fontsize=60, color='white', size=(720, 1280), bg_color='black', method='caption')
        text_clip = text_clip.set_duration(audio.duration).set_position('center')

        video = CompositeVideoClip([text_clip.set_audio(audio)])
        video.write_videofile("short_video.mp4", fps=24)

        os.remove("audio.mp3")
        return jsonify({"status": "success", "message": "Video generated successfully!"})

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
