"""Play audio alerts triggered by MQTT messages."""
import paho.mqtt.client as mqtt
import config
import subprocess
import ssl
import time
from time import sleep
from sys import exit
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

logging.basicConfig(handlers=[RotatingFileHandler(config.log_file, maxBytes=100000, backupCount=3)],
                    format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)
# NOTE: Exceptions related to logging are not handled. It's not like they can be logged :-)

# check all configured sound files exist upon launch.
for sound in config.sounds:
    if not Path(config.sounds[sound]).is_file():
        logging.critical(
            "Audio file path for sound '{}' is incorrect. Exiting.".format(sound))
        exit(1)


def play_alert(sound):
    """Play alert sound using mpg123.

    Parameters:
    sound - name of sound from config.js
    
    Returns:
    mqtt return code
    """

    if config.audiodevice == '':  # use default output device
        return_code = subprocess.run([config.mpg123, config.sounds[sound]],
                                     stderr=subprocess.DEVNULL).returncode
    else:
        return_code = subprocess.run([config.mpg123, '-a', config.audiodevice, config.sounds[sound]],
                                     stderr=subprocess.DEVNULL).returncode  # use specified output device
    return return_code


def time_check():
    """Check whether sounds are allowed to play right now.

    Paremeters:
    None

    Returns:
    True/False
    """
    
    allowed = False
    time_now = time.strftime('%H:%M', time.localtime())
    for times in config.active_times:
        if time_now >= times[0] and time_now <= times[1]:
            allowed = True
            break
    return allowed


def on_connect(client, userdata, flags, rc):
    """Subscribe to topic on connect."""
    if rc == 0:
        logging.info("Connected")
    else:
        logging.warning("Connection issue - result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(config.topic)


def on_message(client, userdata, msg):
    """Process incoming message from MQTT broker. Play sound."""
    if time_check():
        try:
            return_code = play_alert(msg.payload.decode('UTF-8'))
        except FileNotFoundError:
            logging.critical("mpg123 not found. Exiting.")
            exit(1)
        except KeyError:
            logging.warning("Requested sound not recognised.")
        else:
            if return_code < 0:
                logging.error("mpg123 error.")
    else:
        logging.warning("Sounds are not permitted at this time.")


if config.client_id == '':
    client = mqtt.Client()
else:
    client = mqtt.Client(config.client_id)

client.on_connect = on_connect
client.on_message = on_message

if config.cert != '':
    try:
        client.tls_set(config.cert, tls_version=ssl.PROTOCOL_TLSv1_2)
    except FileNotFoundError:
        logging.critical(
            "Configured CA certificate not found. Exiting.")
        exit(1)

    client.tls_insecure_set(False)
if config.username != '':
    client.username_pw_set(config.username, config.password)

# Keep trying to connect until it succeeds
attempt = 0
connection_retry_delay = 60
while True:
    try:
        client.connect(config.mqtt_host, config.mqtt_port, 60)
    except OSError:
        attempt += 1
        logging.warning("Connection attempt #{} failed (waiting {}s).".format(
            attempt, connection_retry_delay))
        sleep(connection_retry_delay)
        continue
    except ssl.CertificateError:
        logging.critical(
            "There is a problem with the SSL certificate. Exiting.")
        exit(1)
    else:
        break

client.loop_forever()
