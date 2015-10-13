# LTUAssistant
An AI assistant like Google Now, Siri, Cortana, etc. for an LTU senior project.

This project depends on the following:
- `espeak` for audio output
- [stanford_corenlp_pywrapper][1] for natural language processing
- The Stanford CoreNLP jar files
- Java (to run Stanford CoreNLP)
- The Python [SpeechRecognition][2] module for voice input
  - This might also require that the PyAudio packages are installed. On Ubuntu,
  this can be done by running `sudo apt-get install python-pyaudio python3-pyaudio`.
  - It also may require flac command line tools. On Ubuntu, this can
  be done by running `sudo apt-get install flac`
All of these are downloaded and installed by setup.py, as long as you have git installed.

It currently runs on Ubuntu-based Linux systems, though we would like to
implement cross-platform functionality soon.

The main program is located in `integrated.py` at the moment.

## Features
This AI assistant aims to be like other well-known AI assistants, but with a
focus on being useful to students. Thus, the feature set will concentrate on
this particular target user.

Some abilities the AI assistant will include are:
- Ability to go to school websites via voice command
- Ability to email professors and classmates using LTU webmail
- Room locator for a given room number (i.e., building and floor)
- Study assistant using user-defined "note cards" to help students prepare for
exams and quizzes
- Reminding the user of upcoming class times

This list may expand based on whatever we have time to implement.

## How it works
This assistant is structured into three main parts:

1. Speech-to-text module
1. Natural language processing module
1. Command execution and database module

Each part passes its results to the next, providing a logical program flow and
making collaboration between our group members easier.

  [1]: https://github.com/brendano/stanford_corenlp_pywrapper
  [2]: https://pypi.python.org/pypi/SpeechRecognition/
