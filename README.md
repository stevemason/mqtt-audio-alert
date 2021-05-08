MQTT-AUDIO-ALERT
================

This project allows audio alerts to be triggered by MQTT messages.

mpg123 was chosen as an audio player as it allowed easy configuration of which output device to use. In my case, I wanted the alert sounds to come out of the headphone jack of a Raspberry Pi - not the HDMI output which I had configured as default. Setting 'audiodevice' to 'hw:1,0' in config.py achieved this for me.

Usage
-----

Settings are configured in 'config.py'. An example file has been provided for you (config_example.py). Please take a look at this file for configuration guidance.

TLS connections to the MQTT broker are supported, but optional.

No audio files are provided - you'll need to bring your own MP3s and reference them in config.py.

To avoid being bothered by alerts e.g. when you're trying to sleep, you can specify permitted alerting times in config.py. You can specify as many time ranges as you like, according to your needs.

Limitations
-----------

Only one MQTT broker and one MQTT topic are currently supported.

Only exact matches with MQTT messages are supported. There is NO support for ranges e.g. 'play sound x if message value is less than y'.

Dependencies
------------

* mpg123 (can be installed with any Linux distro package manager)
* paho-mqtt (can be installed with pip)
