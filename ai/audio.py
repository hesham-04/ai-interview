import pyttsx3
from ai.models import Question
import os

def generate_all_audio():
    engine = pyttsx3.init()
    os.makedirs("media/audio", exist_ok=True)

    for q in Question.objects.all():
        path = f'media/audio/question_{q.id}.mp3'
        engine.save_to_file(q.text, path)
        q.audio_file.name = path.replace('media/', '')
        q.save()

    engine.runAndWait()
    print("✅ All audio generated.")
