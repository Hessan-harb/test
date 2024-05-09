import logging
from pathlib import Path

import click
import speech_recognition as sr
from moviepy.editor import VideoFileClip

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

RESULT_FILE = "recognized.txt"
VIDEO_FILE = "./v.mp4"  # Set the path to your video file here

def video_to_text(video_file: str, output_file: str, language: str = "ar-AR", duration: float = None, offset: float = None, verbose: bool = False) -> None:
    recognizer = sr.Recognizer()

    # Load the video file using moviepy
    video_clip = VideoFileClip(video_file)

    # Extract audio and save it as a temporary WAV file
    audio_path = "temp_audio.wav"
    with video_clip.audio as audio_clip:
        audio_clip.write_audiofile(audio_path)

    # Use SpeechRecognition to recognize speech from the audio file
    logging.info("Converting audio to text. This may take some time...")

    try:
        recognized_text = ""
        with sr.AudioFile(audio_path) as source:
            audio_data = recognizer.record(source, duration=duration, offset=offset)
            logging.info("Audio duration:", video_clip.duration)  # Log audio duration for diagnostics
            recognized_text = recognizer.recognize_google(audio_data, language=language)
            logging.info("Recognized Text:", recognized_text)  # Log recognized text for debugging
    except sr.UnknownValueError:
        logging.error("Speech recognition could not understand audio.")
    except sr.RequestError as e:
        logging.error(f"Error occurred while accessing Google Speech Recognition service: {e}")
    finally:
        # Clean up temporary audio file
        if Path(audio_path).exists():
            Path(audio_path).unlink()

    # Write the recognized text to the output file
    if recognized_text:
        with open(output_file, "w") as file:
            file.write("Recognized Speech:\n")
            file.write(recognized_text)
        logging.info(f"Done! Recognized text saved to {output_file}")
    else:
        logging.warning("No recognized text to write to the output file.")

@click.command("video-to-text")
@click.option("--language", "-lang", default="ar-AR", help="Audio language for speech recognition")
@click.option("--output", "-o", default=RESULT_FILE, help="Output file path for recognized text")
@click.option("--duration", type=float, help="Audio length [seconds]")
@click.option("--offset", type=float, help="Offset from start [seconds]")
@click.option("--verbose", is_flag=True, help="Enable verbose logging for diagnostics")
def main(language: str, output: str, duration: float, offset: float, verbose: bool) -> None:
    if not Path(VIDEO_FILE).exists():
        logging.error("Video file does not exist.")
        return

    # Convert video to text
    video_to_text(VIDEO_FILE, output, language, duration, offset, verbose)

if __name__ == "__main__":
    main()
