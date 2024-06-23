import PyPDF2
import pyttsx3
import os
import tempfile
from PyPDF2 import utils

def extract_text_from_pdf(pdf_file):
    """
    Function to extract text content from a PDF file.
    """
    pdf_reader = PyPDF2.PdfFileReader(pdf_file)
    text = ''
    for page_num in range(pdf_reader.numPages):
        page = pdf_reader.getPage(page_num)
        text += page.extractText()
    return text

def create_audio_book(pdf_path, output_path, voice_gender='female', speech_rate=150):
    """
    Function to create an audiobook from a PDF file.
    """
    try:
        with open(pdf_path, 'rb') as pdf_file:
            text = extract_text_from_pdf(pdf_file)

        speaker = pyttsx3.init()

        voices = speaker.getProperty('voices')
        if voice_gender.lower() == 'male':
            speaker.setProperty('voice', voices[0].id)  # Male voice
        elif voice_gender.lower() == 'female':
            speaker.setProperty('voice', voices[1].id)  # Female voice

        speaker.setProperty('rate', speech_rate)

        temp_wav_file = tempfile.NamedTemporaryFile(delete=False, suffix='.wav')
        temp_wav_file.close()
        speaker.save_to_file(text, temp_wav_file.name)
        speaker.runAndWait()

        os.system(f'ffmpeg -i "{temp_wav_file.name}" -codec:a libmp3lame -qscale:a 2 "{output_path}"')

        os.remove(temp_wav_file.name)

        print(f"Audiobook created successfully: {output_path}")

    except utils.PdfReadError as e:
        print(f"Error reading PDF file: {e}")
    except Exception as e:
        print(f"Error creating audiobook: {e}")

pdf_path = 'file.pdf'
output_audio_path = 'output.mp3'
create_audio_book(pdf_path, output_audio_path, voice_gender='female', speech_rate=150)
