from flask import Flask, request, jsonify
from gtts import gTTS
from moviepy.editor import TextClip, CompositeVideoClip, AudioFileClip
import os
import random
import string

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return "✅ Hindi Shorts Bot is Live! Use POST /generate to submit your topic."

@app.route('/generate', methods=['POST'])
def generate():
    data = request.get_json()

    text = data.get("text")
    lang = data.get("lang", "hi")

    if not text:
        return jsonify({"error": "Text is required"}), 400

    filename = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
    audio_path = f"{filename}.mp3"
    video_path = f"{filename}.mp4"

    tts = gTTS(text=text, lang=lang)
    tts.save(audio_path)

    audio_clip = AudioFileClip(audio_path)
    text_clip = TextClip(
        text,
        fontsize=60,
        color='white',
        size=(720, 1280),
        bg_color='black',
        method='caption'
    ).set_duration(audio_clip.duration).set_position("center")

    final_video = CompositeVideoClip([text_clip.set_audio(audio_clip)])
    final_video.write_videofile(video_path, fps=24)

    os.remove(audio_path)

    return jsonify({"message": "Short video created", "video": video_path})

if __name__ == '__main__':
    app.run(debug=True)

