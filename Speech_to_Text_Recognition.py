import speech_recognition as sr
import pyttsx3
import tkinter as tk
from tkinter import scrolledtext
import threading
import time

class SpeechToTextApp:
    def __init__(self, master):
        self.master = master
        master.title("Speech To Text")
        master.geometry("500x600")
        master.configure(bg='#f0f0f0')

        # Initialize the recognizer and text-to-speech engine
        self.r = sr.Recognizer()
        self.engine = pyttsx3.init()

        # Create main frame
        self.main_frame = tk.Frame(master, bg='#f0f0f0')
        self.main_frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)

        # Title Label
        self.title_label = tk.Label(
            self.main_frame, 
            text="Speech To Text", 
            font=("Helvetica", 20, "bold"), 
            bg='#f0f0f0', 
            fg='#333333'
        )
        self.title_label.pack(pady=(0, 20))

        # Listen Button
        self.listen_button = tk.Button(
            self.main_frame, 
            text="Start Listening", 
            command=self.start_listening,
            bg='#4CAF50', 
            fg='white', 
            font=("Helvetica", 14),
            width=20,
            relief=tk.RAISED
        )
        self.listen_button.pack(pady=10)

        # Status Label
        self.status_label = tk.Label(
            self.main_frame, 
            text="Click 'Start Listening' to begin", 
            font=("Helvetica", 12), 
            bg='#f0f0f0', 
            fg='#666666'
        )
        self.status_label.pack(pady=10)

        # Conversation Text Area
        self.conversation_text = scrolledtext.ScrolledText(
            self.main_frame, 
            wrap=tk.WORD, 
            width=50, 
            height=15, 
            font=("Consolas", 10)
        )
        self.conversation_text.pack(pady=10)

        # Flag to control listening
        self.is_listening = False

    def SpeakText(self, command):
        try:
            self.engine.say(command)
            self.engine.runAndWait()
        except Exception as e:
            self.update_status(f"Error in speech synthesis: {e}")

    def update_status(self, message):
        self.status_label.config(text=message)
        self.conversation_text.insert(tk.END, message + "\n")
        self.conversation_text.see(tk.END)

    def listen_continuously(self):
        while self.is_listening:
            try:
                with sr.Microphone() as source2:
                    self.r.adjust_for_ambient_noise(source2, duration=0.5)
                    self.update_status("Listening... Speak now!")

                    # Listen until the speaker stops talking
                    audio2 = self.r.listen(source2, timeout=3, phrase_time_limit=5)

                    try:
                        # Recognize speech using Google Web Speech API
                        MyText = self.r.recognize_google(audio2, language="en-IN")
                        MyText = MyText.lower()

                        # Update conversation and speak
                        self.update_status(f"You said: {MyText}")
                        self.SpeakText(MyText)

                        # Stop the process if the user says "stop it"
                        if MyText == "stop it":
                            self.is_listening = False
                            self.listen_button.config(state=tk.NORMAL)
                            self.update_status("Listening stopped.")
                            break

                    except sr.UnknownValueError:
                        self.update_status("Sorry, I couldn't understand that. Please try again.")
                    except sr.RequestError as e:
                        self.update_status(f"Could not request results; {e}")

            except sr.WaitTimeoutError:
                self.update_status("No speech detected. Resuming listening...")
            except Exception as e:
                self.update_status(f"An error occurred: {e}")

    def start_listening(self):
        if not self.is_listening:
            self.is_listening = True
            self.listen_button.config(state=tk.DISABLED)
            
            # Start listening in a separate thread
            threading.Thread(target=self.listen_continuously, daemon=True).start()

def main():
    root = tk.Tk()
    app = SpeechToTextApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()