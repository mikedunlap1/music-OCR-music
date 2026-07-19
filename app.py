import gradio as gr
import os, glob, tempfile
from music21 import converter
from midi2audio import FluidSynth

SOUNDFONT_PATH = "/usr/share/sounds/sf2/FluidR3_GM.sf2"

def process(uploaded_file):
    if uploaded_file is None:
        return None, None, None, "Please upload an image."

    # Raw uploaded file, untouched (this is the fix that stopped the crash)
    image_path = uploaded_file if isinstance(uploaded_file, str) else uploaded_file.name

    outdir = tempfile.mkdtemp()
    os.system(f'oemer "{image_path}" -o {outdir}')

    xmls = glob.glob(os.path.join(outdir, "*.musicxml")) + \
           glob.glob(os.path.join(outdir, "*.xml"))
    if not xmls:
        return None, None, None, "oemer couldn't read this image. Try another."
    xml_path = xmls[0]

    # MusicXML -> MIDI
    midi_path = os.path.join(outdir, "result.mid")
    try:
        converter.parse(xml_path).write("midi", fp=midi_path)
    except Exception as e:
        return xml_path, None, None, f"Got MusicXML, but MIDI failed: {e}"

    # MIDI -> WAV
    wav_path = os.path.join(outdir, "result.wav")
    try:
        FluidSynth(SOUNDFONT_PATH).midi_to_audio(midi_path, wav_path)
    except Exception as e:
        return xml_path, midi_path, None, f"Got MusicXML + MIDI, but audio failed: {e}"

    return xml_path, midi_path, wav_path, "Done ✅"

demo = gr.Interface(
    fn=process,
    inputs=gr.File(label="Upload Sheet Music Image", file_types=["image"]),
    outputs=[
        gr.File(label="MusicXML (.musicxml)"),
        gr.File(label="MIDI (.mid)"),
        gr.Audio(label="Audio (.wav)"),
        gr.Textbox(label="Status"),
    ],
    title="Sheet Music → MusicXML / MIDI / Audio",
    description="Upload a sheet music image to get notation, MIDI, and playable audio.",
)

demo.launch(server_name="0.0.0.0", server_port=int(os.environ.get("PORT", 7860)))
