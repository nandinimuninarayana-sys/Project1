#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import os
import speech_recognition as sr
from googletrans import Translator
from gtts import gTTS
import noisereduce as nr
import numpy as np

class SpeechProcessor:
    def __init__(self):
        self.language_names = {
            "af": "Afrikaans", "sq": "Albanian", "am": "Amharic", "ar": "Arabic", "hy": "Armenian",
            "az": "Azerbaijani", "eu": "Basque", "be": "Belarusian", "bn": "Bengali", "bs": "Bosnian",
            "bg": "Bulgarian", "ca": "Catalan", "ceb": "Cebuano", "ny": "Chichewa", "zh-CN": "Chinese (Simplified)",
            "zh-TW": "Chinese(tr)", "co": "Corsican", "hr": "Croatian", "cs": "Czech", "da": "Danish",
            "nl": "Dutch", "en": "English", "eo": "Esperanto", "et": "Estonian", "tl": "Filipino", "fi": "Finnish",
            "fr": "French", "fy": "Frisian", "gl": "Galician", "ka": "Georgian", "de": "German", "el": "Greek",
            "gu": "Gujarati", "ht": "Haitian Creole", "ha": "Hausa", "haw": "Hawaiian", "iw": "Hebrew", "hi": "Hindi",
            "hmn": "Hmong", "hu": "Hungarian", "is": "Icelandic", "ig": "Igbo", "id": "Indonesian", "ga": "Irish",
            "it": "Italian", "ja": "Japanese", "jw": "Javanese", "kn": "Kannada", "kk": "Kazakh", "km": "Khmer",
            "ko": "Korean", "ku": "Kurdish (Kurmanji)", "ky": "Kyrgyz", "lo": "Lao", "la": "Latin", "lv": "Latvian",
            "lt": "Lithuanian", "lb": "Luxembourgish", "mk": "Macedonian", "mg": "Malagasy", "ms": "Malay",
            "ml": "Malayalam", "mt": "Maltese", "mi": "Maori", "mr": "Marathi", "mn": "Mongolian", "my": "Myanmar (Burmese)",
            "ne": "Nepali", "no": "Norwegian", "or": "Odia (Oriya)", "ps": "Pashto", "fa": "Persian", "pl": "Polish",
            "pt": "Portuguese", "pa": "Punjabi", "ro": "Romanian", "ru": "Russian", "sm": "Samoan", "gd": "Scots Gaelic",
            "sr": "Serbian", "st": "Sesotho", "sn": "Shona", "sd": "Sindhi", "si": "Sinhala", "sk": "Slovak",
            "sl": "Slovenian", "so": "Somali", "es": "Spanish", "su": "Sundanese", "sw": "Swahili", "sv": "Swedish",
            "tg": "Tajik", "ta": "Tamil", "te": "Telugu", "th": "Thai", "tr": "Turkish", "uk": "Ukrainian",
            "ur": "Urdu", "ug": "Uyghur", "uz": "Uzbek", "vi": "Vietnamese", "cy": "Welsh", "xh": "Xhosa",
            "yi": "Yiddish", "yo": "Yoruba", "zu": "Zulu"
        }

    def greet(self):
        print("\033[1;35;40mFabulous Speech-Text processor\033[m")

    def display_options(self):
        print("\033[1;30;43m 1) Text-to-Speech \033[m")
        print("\033[1;30;43m 2) Speech-to-Text \033[m")

    def text_to_speech(self):
        text = input("\033[1;33;40mEnter the text: \033[m")
        languages = self.input_languages()

        try:
            for i in range(0, len(languages), 3):
                for j in range(3):
                    if i + j < len(languages):
                        language = languages[i + j]
                        translated_text = ""  # Initialize translated_text variable

                        # Perform translation if needed
                        if language != "en":
                            translator = Translator()
                            translated_text = translator.translate(text, src="en", dest=language).text
                            print(f"\033[1;44;37mTranslated Text ({language.upper()}): \033[m", translated_text)

                        # Text-to-speech conversion
                        tts = gTTS(text=translated_text if translated_text else text, lang=language, slow=False)
                        tts.save("output.mp3")

                        # Play the generated audio
                        os.system("start output.mp3")

        except Exception as e:
            print(f"An error occurred: {e}")

    def speech_to_text(self):
        languages = self.input_languages()

        try:
            for i in range(0, len(languages), 3):
                for j in range(3):
                    if i + j < len(languages):
                        language = languages[i + j]
                        recognizer = sr.Recognizer()

                        with sr.Microphone() as source:
                            print(f"\033[1;35;40mSpeak something in {language.upper()}...\033[m")
                            audio = recognizer.listen(source)

                            # Convert the audio to numpy array
                            audio_data = np.frombuffer(audio.frame_data, dtype=np.int16)

                            # Perform noise reduction
                            reduced_noise = nr.reduce_noise(audio_data, audio.sample_rate)

                        # Create a new audio source from the noise-reduced signal
                        noise_reduced_audio = sr.AudioData(reduced_noise.tobytes(), sample_rate=audio.sample_rate, sample_width=2)

                        text = recognizer.recognize_google(noise_reduced_audio, language=language)
                        print(f"\033[1;32;40mText ({language.upper()}): \033[m", text)

                        # Translation to English
                        if language != "en":
                            translator = Translator()
                            translated_text = translator.translate(text, dest="en").text
                            print("\033[1;44;37mTranslated Text (English): \033[m", translated_text)
                        
                        print("\033[1;40;33mRecorded Successfully\033[m")  # Message with different color background

        except sr.UnknownValueError:
            print("\033[1;31;40mCould not understand audio\033[m")
        except sr.RequestError as e:
            print(f"\033[1;31;40mError making the request: {e}\033[m")

    def input_languages(self):
        print("\033[1;33;40mSelect Language:\033[m")
        for code, name in self.language_names.items():
            print(f"\033[1;34;40m{code}:\033[1;30;46m{name.ljust(15)}\033[m", end="\t")
            if (list(self.language_names.keys()).index(code) + 1) % 5 == 0:
                print()

        language_codes = input("\033[1;33;40mEnter the language codes: \033[m").split()
        for code in language_codes:
            while code not in self.language_names:
                print("\033[1;31;40mInvalid language code. Please try again.\033[m")
                language_codes = input("\033[1;33;40mEnter the language codes: \033[m").split()

        return language_codes

    def main(self):
        self.greet()
        while True:
            self.display_options()
            choice = input("\033[1;35;40mChoose an option (1/2): \033[m")

            if choice == "1":
                self.text_to_speech()
            elif choice == "2":
                self.speech_to_text()
            else:
                print("\033[1;31;40mInvalid choice. Please enter 1 or 2.\033[m")

            continue_option = input("\033[1;33;40mDo you want to continue? (yes/no): \033[m").lower()
            if continue_option != "yes":
                print("\033[1;32;40mExiting the program. Goodbye!\033[m")
                break

if __name__ == "__main__":
    processor = SpeechProcessor()
    processor.main()


# In[2]:


get_ipython().system('pip install noisereduce')



# In[4]:


import os
import speech_recognition as sr
from googletrans import Translator
from gtts import gTTS
import noisereduce as nr
import numpy as np

class SpeechProcessor:
    def __init__(self):
        self.language_names = {
            "af": "Afrikaans", "sq": "Albanian", "am": "Amharic", "ar": "Arabic", "hy": "Armenian",
            "az": "Azerbaijani", "eu": "Basque", "be": "Belarusian", "bn": "Bengali", "bs": "Bosnian",
            "bg": "Bulgarian", "ca": "Catalan", "ceb": "Cebuano", "ny": "Chichewa", "zh-CN": "Chinese (Simplified)",
            "zh-TW": "Chinese(tr)", "co": "Corsican", "hr": "Croatian", "cs": "Czech", "da": "Danish",
            "nl": "Dutch", "en": "English", "eo": "Esperanto", "et": "Estonian", "tl": "Filipino", "fi": "Finnish",
            "fr": "French", "fy": "Frisian", "gl": "Galician", "ka": "Georgian", "de": "German", "el": "Greek",
            "gu": "Gujarati", "ht": "Haitian Creole", "ha": "Hausa", "haw": "Hawaiian", "iw": "Hebrew", "hi": "Hindi",
            "hmn": "Hmong", "hu": "Hungarian", "is": "Icelandic", "ig": "Igbo", "id": "Indonesian", "ga": "Irish",
            "it": "Italian", "ja": "Japanese", "jw": "Javanese", "kn": "Kannada", "kk": "Kazakh", "km": "Khmer",
            "ko": "Korean", "ku": "Kurdish (Kurmanji)", "ky": "Kyrgyz", "lo": "Lao", "la": "Latin", "lv": "Latvian",
            "lt": "Lithuanian", "lb": "Luxembourgish", "mk": "Macedonian", "mg": "Malagasy", "ms": "Malay",
            "ml": "Malayalam", "mt": "Maltese", "mi": "Maori", "mr": "Marathi", "mn": "Mongolian", "my": "Myanmar (Burmese)",
            "ne": "Nepali", "no": "Norwegian", "or": "Odia (Oriya)", "ps": "Pashto", "fa": "Persian", "pl": "Polish",
            "pt": "Portuguese", "pa": "Punjabi", "ro": "Romanian", "ru": "Russian", "sm": "Samoan", "gd": "Scots Gaelic",
            "sr": "Serbian", "st": "Sesotho", "sn": "Shona", "sd": "Sindhi", "si": "Sinhala", "sk": "Slovak",
            "sl": "Slovenian", "so": "Somali", "es": "Spanish", "su": "Sundanese", "sw": "Swahili", "sv": "Swedish",
            "tg": "Tajik", "ta": "Tamil", "te": "Telugu", "th": "Thai", "tr": "Turkish", "uk": "Ukrainian",
            "ur": "Urdu", "ug": "Uyghur", "uz": "Uzbek", "vi": "Vietnamese", "cy": "Welsh", "xh": "Xhosa",
            "yi": "Yiddish", "yo": "Yoruba", "zu": "Zulu"
        }

    def greet(self):
        print("\033[1;35;40mFabulous Speech-Text processor\033[m")

    def display_options(self):
        print("\033[1;30;43m 1) Text-to-Speech \033[m")
        print("\033[1;30;43m 2) Speech-to-Text \033[m")

    def text_to_speech(self):
        text = input("\033[1;33;40mEnter the text: \033[m")
        languages = self.input_languages()

        try:
            for i in range(0, len(languages), 3):
                for j in range(3):
                    if i + j < len(languages):
                        language = languages[i + j]
                        translated_text = ""  # Initialize translated_text variable

                        # Perform translation if needed
                        if language != "en":
                            translator = Translator()
                            translated_text = translator.translate(text, src="en", dest=language).text
                            print(f"\033[1;44;37mTranslated Text ({language.upper()}): \033[m", translated_text)

                        # Text-to-speech conversion
                        tts = gTTS(text=translated_text if translated_text else text, lang=language, slow=False)
                        tts.save("output.mp3")

                        # Play the generated audio
                        os.system("start output.mp3")

        except Exception as e:
            print(f"An error occurred: {e}")

    def speech_to_text(self):
        languages = self.input_languages()

        try:
            for i in range(0, len(languages), 3):
                for j in range(3):
                    if i + j < len(languages):
                        language = languages[i + j]
                        recognizer = sr.Recognizer()

                        with sr.Microphone() as source:
                            print(f"\033[1;35;40mSpeak something in {language.upper()}...\033[m")
                            audio = recognizer.listen(source)

                            # Convert the audio to numpy array
                            audio_data = np.frombuffer(audio.frame_data, dtype=np.int16)

                            # Perform noise reduction
                            reduced_noise = nr.reduce_noise(audio_data, audio.sample_rate)

                        # Create a new audio source from the noise-reduced signal
                        noise_reduced_audio = sr.AudioData(reduced_noise.tobytes(), sample_rate=audio.sample_rate, sample_width=2)

                        text = recognizer.recognize_google(noise_reduced_audio, language=language)
                        print(f"\033[1;32;40mText ({language.upper()}): \033[m", text)

                        # Translation to English
                        if language != "en":
                            translator = Translator()
                            translated_text = translator.translate(text, dest="en").text
                            print("\033[1;44;37mTranslated Text (English): \033[m", translated_text)
                        
                        print("\033[1;40;33mRecorded Successfully\033[m")  # Message with different color background

        except sr.UnknownValueError:
            print("\033[1;31;40mCould not understand audio\033[m")
        except sr.RequestError as e:
            print(f"\033[1;31;40mError making the request: {e}\033[m")

    def input_languages(self):
        print("\033[1;33;40mSelect Language:\033[m")
        for code, name in self.language_names.items():
            print(f"\033[1;34;40m{code}:\033[1;30;46m{name.ljust(15)}\033[m", end="\t")
            if (list(self.language_names.keys()).index(code) + 1) % 5 == 0:
                print()

        language_codes = input("\033[1;33;40mEnter the language codes: \033[m").split()
        for code in language_codes:
            while code not in self.language_names:
                print("\033[1;31;40mInvalid language code. Please try again.\033[m")
                language_codes = input("\033[1;33;40mEnter the language codes: \033[m").split()

        return language_codes

    def main(self):
        self.greet()
        while True:
            self.display_options()
            choice = input("\033[1;35;40mChoose an option (1/2): \033[m")

            if choice == "1":
                self.text_to_speech()
            elif choice == "2":
                self.speech_to_text()
            else:
                print("\033[1;31;40mInvalid choice. Please enter 1 or 2.\033[m")

            continue_option = input("\033[1;33;40mDo you want to continue? (yes/no): \033[m").lower()
            if continue_option != "yes":
                print("\033[1;32;40mExiting the program. Goodbye!\033[m")
                break

if __name__ == "__main__":
    processor = SpeechProcessor()
    processor.main()


# In[ ]:





# In[ ]:




