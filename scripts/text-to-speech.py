import os
import re
import sys
import json
import torch
import torchaudio as ta
from chatterbox.tts import ChatterboxTTS


def normalize_text(text):
    # Replace punctuation that TTS models handle poorly
    text = text.replace("\u2014", ", ")  # em dash —
    text = text.replace("\u2013", ", ")  # en dash –
    text = text.replace("\u2018", "'").replace("\u2019", "'")  # curly single quotes
    text = text.replace("\u201c", '"').replace("\u201d", '"')  # curly double quotes
    return text


def split_sentences(text):
    # Split on sentence-ending punctuation, keeping the delimiter
    sentences = re.split(r'(?<=[.!?])\s+', text.strip())
    return [s for s in sentences if s]

# Input JSON format:
# {
#     "segments": [
#         {"character": "interviewer", "text": "Welcome to the show."},
#         {"character": "interviewee", "text": "Thanks for having me."}
#     ]
# }

VOICES_DIR = os.path.join(os.path.dirname(__file__), "..", "voices", "short")

characters = {
    "interviewer": os.path.join(VOICES_DIR, "f-sa.wav"),
    "interviewee": os.path.join(VOICES_DIR, "stephen.wav"),
}

INPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "input")
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "output")

if len(sys.argv) > 1:
    json_filename = sys.argv[1]
else:
    json_filename = input("Enter input JSON filename: ").strip()

if not json_filename.endswith(".json"):
    json_filename += ".json"

input_path = os.path.join(INPUT_DIR, json_filename)
output_path = os.path.join(OUTPUT_DIR, os.path.splitext(json_filename)[0] + ".wav")

with open(input_path, "r", encoding="utf-8") as f:
    data = json.load(f)

model = ChatterboxTTS.from_pretrained(device="cuda")

between_segments_silence = torch.zeros(1, int(model.sr * 0.5))
between_sentences_silence = torch.zeros(1, int(model.sr * 0.2))

audio_chunks = []
segments = data["segments"]
for i, segment in enumerate(segments):
    character = segment["character"]
    voice_ref = characters[character]
    sentences = split_sentences(normalize_text(segment["text"]))
    for j, sentence in enumerate(sentences):
        print(f"[{i+1}/{len(segments)}] {character}: {sentence}")
        wav = model.generate(sentence, audio_prompt_path=voice_ref)
        audio_chunks.append(wav)
        if j < len(sentences) - 1:
            audio_chunks.append(between_sentences_silence)
    if i < len(segments) - 1:
        audio_chunks.append(between_segments_silence)

final_audio = torch.cat(audio_chunks, dim=-1)
ta.save(output_path, final_audio, model.sr)

# TODO: convert to MP3 using pydub (requires ffmpeg on PATH)
# mp3_path = os.path.splitext(output_path)[0] + ".mp3"
# AudioSegment.from_wav(output_path).export(mp3_path, format="mp3")
# os.remove(output_path)
print(f"Saved to {output_path}")
