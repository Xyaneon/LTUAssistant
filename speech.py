#!/usr/bin/env python3

# NOTE: this example requires PyAudio because it uses the Microphone class

import notify2
import speech_recognition as sr
import subprocess

notify2.init('LTU Assistant')

def listen():
    # obtain audio from the microphone
    r = sr.Recognizer()
    ret = ""
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        print("Say something!")
        audio = r.listen(source)

    # recognize speech using Google Speech Recognition
    try:
        # for testing purposes, we're just using the default API key
        # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
        # instead of `r.recognize_google(audio)`
        print("Got text, sending to Google")
        sentence = r.recognize_google(audio)
        print("Google Speech Recognition thinks you said " + r.recognize_google(audio))
        return True, sentence
    except sr.UnknownValueError:
        ret = "Google Speech Recognition could not understand audio"
    except sr.RequestError:
        ret = "Could not request results from Google Speech Recognition service"
    return False, ret

def speak(message, also_cmd=False):
    '''Speak the given message using the text-to-speech backend.'''
    if also_cmd:
        print(message)
    notification = notify2.Notification('LTU Assistant',
                                        message,
                                        'notification-message-im')
    notification.show()
    subprocess.call('espeak "' + message + '"', shell=True)

def ask_question(question, also_cmd=False):
    '''Ask the user a question and return the reply as a string.'''
    speak(question, also_cmd)
    num_tries = 3
    for x in range(0, num_tries):
        (success, sentence) = listen()
        if success:
            return sentence
        else:
            speak('I\'m sorry, could you repeat that?', also_cmd)
    speak('I\'m sorry, I could not understand you.', also_cmd)
    return ''

if __name__ == '__main__':
    (success, error) = listen()
    if not success:
        print(error)
