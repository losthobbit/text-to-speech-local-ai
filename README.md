# text-to-speech-local-ai

Local AI text-to-speech using [Chatterbox TTS](https://github.com/resemble-ai/chatterbox), with support for multi-character conversations.

## Requirements

- Python 3.10+
- CUDA-capable GPU
- Dependencies: `pip install -r requirements.txt`

## Setup

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

## Usage

Place a JSON conversation file in the `input/` folder, then run:

```bash
python scripts/text-to-speech.py myconversation.json
```

Or run without arguments to be prompted for the filename:

```bash
python scripts/text-to-speech.py
```

Output is saved to `output/` as a `.wav` file with the same name as the input.

## Input Format

```json
{
    "segments": [
        {"character": "interviewer", "text": "Welcome to the show."},
        {"character": "interviewee", "text": "Thanks for having me."}
    ]
}
```

## Characters

| Character | Voice reference |
|-----------|----------------|
| `interviewer` | `voices/short/f-sa.wav` |
| `interviewee` | `voices/short/stephen.wav` |

To add a character, add an entry to the `characters` dict in `scripts/text-to-speech.py` and place the reference WAV in `voices/short/`.
