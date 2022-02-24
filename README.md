# WPM Meter

The project should contain a README that explains how to run the product and what approach they took to solve the problem.

## How to run

### Prerequisites
(I'll leave my api_key available to make this less painful so you can skip first 3 steps)
1) Sign up for AssemblyAI - https://app.assemblyai.com/signup
2) Upgrade your account so you can use the live transcription feature - https://app.assemblyai.com/billing
3) Add your API key (available [here](https://app.assemblyai.com/account)) to `.env` under `API_KEY`


### Running the terminal app
1) Install portaudio, for macOS `brew install portaudio`. Note: this app will not work on WSL since it is currently unable to utilize the audio interfaces of Windows. For more information, check http://files.portaudio.com/download.html.
2) Change the cwd to project root
3) Create a new python environment `python -m venv env`
4) Activate the new environment `source /env/bin/activate`
5) Install required libraries and dependencies `pip install -r requirements.txt`
6) Run the terminal app `python wpm_meter.py`

To stop the terminal app, use control + C.


## Features
- Track your WPM rate in real time.
- Get color coded indicators saying if you are talking too slowly or too quickly.
- Get completed sentences in the terminal output.
- Choose which input device you want to use.
- Have all completed sentences stores in a text file.


## Problems I faced / Approach I took
- Did some reseach and was able to find [this](https://www.assemblyai.com/blog/real-time-speech-recognition-with-python/?_ga=2.123253452.639823529.1645689349-1924652623.1645689349&_gac=1.61762270.1645689349.Cj0KCQiA09eQBhCxARIsAAYRiyk52jH_9X2eLG9Oiajv9jIrRMQmcTgOihFLa8UFIKsQF-IGhj2NzjcaAo4HEALw_wcB) excellent article which I used as a base concept. It helped me cut down on research time needed for getting to know pyaudio.
- Didn't really get a chance to work with audio in python before, which meant I didn't know a thing about setting it up. My main driver the past couple of months is Windows with WSL through VSCode remote WSL extension. It took me probably about 1.5hrs of research to find out that it's not possible (or it is, but I was just running out of time so I decided to stop going down the rabbit hole). So I switched to macOS and everything just worked (as always).
- Started investigating how everything works and it seemed pretty straightforward. I created some helpers to let the user decide which input device he wants to use, added error handling that assumed the user is not tech savy.
- Added the function to calculate the wpm based on the lenght of the list of words returned via the wss and the difference between start and end times of a transcription block.
- Added a config class that pulls values via python-dotenv from a .env file.
- Implemented slow/quick tresholds and added color to them.
- Refactored prints into logs and added debug logs.
- Figured out how to let the app stop with ^C keyboard interrupt using `asyncio.get_event_loop` and `run_until_complete`
- Added the saving of the final transcription blocks to a txt file.
- Added the obligatory terminal startup ASCII wordart.
- Freezed the pip requirements into requirements.txt
- Took pyaudio init part into helpers to keep `wpm_meter.py` clean.
- Wrote this document.
- Added .gitignore
- Pushed the project to git (probably should have started with this, but I started playing around with the example and kind of drifted off into doing the assignment)


## Summary
- I had a lot of fun doing this, it's pretty impressive how fast and accurate the live transcription is.
- API docs is very helpful and the webapp where I got the key was very intuitive offering great user experience.
- Time took to resolve is around 5-6 hours, although I did have the full functionality in a couple of minutes (after troubleshooting portaudio + pyaudio vs WSL for over an hour).
