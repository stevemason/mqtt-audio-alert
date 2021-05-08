"""Private config items for mqtt-audio-alert."""
sounds = {
    # 'NAMEOFSOUND1': '/PATH/TO/AUDIOFILE.mp3',
    # 'NAMEOFSOUND2': '/PATH/TO/AUDIOFILE.mp3'   
}
# Time ranged where sounds are permitted to play.
# Multiple time ranges are allowed.
active_times = [
    #['07:00', '12:00'],
    #['13:15', '14:15'],
    ['00:00', '23:59']
]

mpg123 = '/usr/bin/mpg123'

#audiodevice = 'hw:1,0'
audiodevice = ''  # leave blank for default device

topic = 'mqtt-audio-alert' # which MQTT topic to subscribe to
client_id = 'mqtt-audio-alert1'  # leave blank for default client_id

mqtt_host = '' # address of MQTT broker
mqtt_port = 1883

log_file = './mqtt-audio-alert.log'

username = ''  # leave blank for no username
password = ''  # leave blank for no password

#cert = "./root-ca.crt"
cert = ''  # leave blank for no TLS
