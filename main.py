# pip install SpeechRecognition PyQt5
# pip install pyaudio
# imports the system module which provides access to some vaiables used
import sys
# this supports for several speech recognition libraries
import speech_recognition as sr
# for GUI support
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QTextEdit
# for GUI support
from PyQt5.QtCore import Qt

class SpeechRecognitionApp(QWidget):
    # constructor
    def __init__(self):
        #This calls the constructor of the parent class
        super().__init__()
        # separate the initialization of the UI components into a separate method 
        self.init_ui()
    # setting up  the UI elements of the PyQt5 application
    def init_ui(self):
        self.setWindowTitle('Arabic Speech Recognition App')
        self.setGeometry(300, 300, 900, 400)
        # display the recognized text
        self.text_edit = QTextEdit()
        # to read only meaning users cannot edit the text
        self.text_edit.setReadOnly(True)
        self.button = QPushButton('Start Recording')
        # called method to start_recording when click it (which is defined down)
        self.button.clicked.connect(self.start_recording)
        # provides a vertical box layout
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.text_edit)
        self.layout.addWidget(self.button)
        self.setLayout(self.layout)

    def start_recording(self):
        self.text_edit.setPlaceholderText('Start Recording...')
        try:
            # set up speech recognition
            recognizer = sr.Recognizer()
            # set up microphone 
            mic = sr.Microphone()
            # prepares the microphone for capturing audio
            with mic as source:
                recognizer.adjust_for_ambient_noise(source)
                audio = recognizer.listen(source)

            self.text_edit.setPlaceholderText('Recognizing...')
            # 
            recognized_text = recognizer.recognize_google(audio, language='ar-AR')

            if recognized_text:
                current_text = self.text_edit.toPlainText()
                if current_text:  # Append to existing text
                    self.text_edit.setPlainText(f'{current_text}\n Text: {recognized_text}')
                else:
                    self.text_edit.setPlainText(f' Text: {recognized_text}')
            else:
                self.text_edit.setPlainText('No speech detected.')

        except sr.UnknownValueError:
            self.text_edit.setPlainText('Sorry, could not understand the audio.')
        except sr.RequestError:
            self.text_edit.setPlainText('Sorry, there was an issue with the service.')
        except Exception as e:
            self.text_edit.setPlainText(f'Error: {str(e)}')

def main():
    app = QApplication(sys.argv)
    window = SpeechRecognitionApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
