# 🎼 Music OCR — Sheet Music → MusicXML, MIDI & Audio

A web app that turns a photo of sheet music into editable notation and playable sound. Upload an image, get back **MusicXML**, **MIDI**, and a rendered **WAV** you can listen to in the browser.

Built with Optical Music Recognition (OMR) — the music equivalent of OCR.

## What it does

1. **Image → MusicXML** — [oemer](https://github.com/BreezeWhite/oemer) reads the notation off the image (staff lines, noteheads, symbols, pitch).
2. **MusicXML → MIDI** — [music21](https://web.mit.edu/music21/) converts the notation to playable MIDI.
3. **MIDI → Audio** — FluidSynth renders the MIDI to a WAV using a General MIDI soundfont.

Wrapped in a [Gradio](https://gradio.app) interface for a simple upload-and-download UI.

## Tech stack

- **OMR / ML:** oemer (ONNX Runtime, CPU)
- **Notation:** music21
- **Audio:** FluidSynth + FluidR3 GM soundfont
- **UI:** Gradio
- **Container:** Docker
- **Hosting:** Render (Docker web service)

## Deploy on Render

This repo is Docker-based, so Render builds it directly — no manual dependency setup.

1. Push these files to a
