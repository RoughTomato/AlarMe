import gi
gi.require_version('Notify', '0.7')
from gi.repository import Notify
from ctypes import *
import pyaudio
import wave
import sys
import time


ERROR_HANDLER_FUNC = CFUNCTYPE(None, c_char_p, c_int, c_char_p, c_int, c_char_p)
def py_error_handler(filename, line, function, err, fmt):
    pass
c_error_handler = ERROR_HANDLER_FUNC(py_error_handler)

Notify.init("Test")
asound = cdll.LoadLibrary('libasound.so')

CHUNK = 1024
asound.snd_lib_error_set_handler(c_error_handler)
wf = wave.open('./sounds/263133.wav','rb')

p = pyaudio.PyAudio()

def callback(in_data, frame_count, time_info, status):
    data = wf.readframes(frame_count)
    return (data, pyaudio.paContinue)

stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                channels=wf.getnchannels(),
                rate=wf.getframerate(),
                output=True,
                stream_callback=callback)

stream.start_stream()

while stream.is_active():
    time.sleep(0.1)

stream.stop_stream()
stream.close()
wf.close()

p.terminate()

Notify.Notification.new("Hi").show()

