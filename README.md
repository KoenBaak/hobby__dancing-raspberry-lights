# hobby__dancing-raspberry-lights
LED Strip connected to a Raspberry PI dancing to music played on another device

This is an old hobby project. Originally created in November 2021 and uploaded
without changes to GitHub in 2023. 

This repo contains three packages

- `pilights` contains code to control a LED strip from a Raspberry Pi. 
The strip I have is the WS2811.
- `lightserver` contains the code for a server that receives an audio stream 
and lets the LED strip dance to this audio. This server should be the Raspberry Pi,
- `audiostreamer` contains the code for an application that streams audio played on 
that device to the lightserver. 

Remarks
- The initial idea was to have the audio play on the Raspberry Pi and let the LED srip
visualize it. However, there were problems with playing audio over aux and managing the LED strip 
simultaneously on the Pi.
- This project is not tested on any other setup then my own. It is probably quite
- senstive to changes in platform, specific LED strip, package versions, etc...
- The actual audio processing to light comes from [this blog post](https://yager.io/LEDStrip/LED.html).

## Config
In the `config.env` file you will need:
- `HOST` the host IP of the lightserver
- `PORT` the host port of the lightserver
- `CHUNK_SIZE` the chunk size in which to stream the audio. This setting is somewhat sensitive.
Making the value to big, will result in bad visualization results, while making it to small, will make
the light go out of sync, as they can not keep up with the stream.
The value 2048 works well for me. 
- `PIN` The pin on the Raspberry Pi at which the LED strip is attached. 
- `NPIXELS` The number of LEDS on the strip. 
- `COLOR_ORDER` The color order of the LED strip. 
- `DEV_INDEX` The audio device on the audiostreamer to use. Should be a loopback device.
If you are on windows, a device can be picked automatically. 

## Running

**On the Raspberry Pi**
(No tested beyond Python 3.7)
- Install the requirements with ``sudo pip install``. You really do need the sudo.
- Run the server with ``sudo python3 -m lightserver``

**On the streaming device**

_Windows_
- Be sure to use a Python 3.7 environment otherwise the PyAudio installation will not work
- Install the requirements. Look at the requirements file first, it contains a link to a PyAudio wheel that
also contains portaudio, this is needed for the loopback mode. 
- Run ``python -m audiostreamer``

_Other_
Not tested. 

![Demo](demo.gif)
