from os import path
import numpy as np
import soundfile as sf
from audio_helpers import play_audio
from librosa.effects import pitch_shift
from librosa.core import load
from librosa.output import write_wav


DIR = 'data/wave'
fn = '2.wav'
base_name, ext = path.splitext(fn)
FN = path.join(DIR, fn)
FN_NEW = path.join(DIR, '{}_shifted{}'.format(base_name, ext))

x, fs = load(FN)
print "Script loaded file with fs {}".format(fs)


def to_pcm(x):
    max_val = np.iinfo(np.int16).max
    return (x * max_val).astype(np.int16)


shifted = pitch_shift(x, fs, 2)
sf.write(FN_NEW, shifted, fs, subtype="PCM_24")
play_audio(FN_NEW)
