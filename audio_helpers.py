from __future__ import print_function

# high-level imports
import os
import time
from os import path
import scipy as sp
import numpy as np
from scipy.io.wavfile import read as wavread, write as wavwrite
from matplotlib import pyplot as plt
import pyaudio
import wave
from scipy import signal
from scipy.interpolate import interp1d
from numpy.fft import fft, fftfreq
import librosa
from librosa.display import waveplot, specshow


def plot_spec(signal, sr=16000, win_length=None, hop_length=None, return_spec=False):
    if win_length is None:
        win_length = int(sr * 0.025)
        
    if hop_length is None:
        hop_length = int(sr * 0.010)
        
    Sxx = librosa.core.stft(
        signal,
        win_length=win_length,
        hop_length=hop_length,
        n_fft=4096
    )

    spec = librosa.amplitude_to_db(np.abs(Sxx), ref=np.max)
    specshow(
        spec,
        sr=sr,
        x_axis='time',
        y_axis='hz',
        cmap='gray_r'
    )
    plt.colorbar(format='%+2.0f dB')
    
    if return_spec:
        return spec
    
    
# Opens the file and plays it via an output audio stream.
def play_audio(file_name):
    wf = wave.open(file_name, 'rb')

    def callback(in_data, frame_count, time_info, status):
        data = wf.readframes(frame_count)
        return (data, pyaudio.paContinue)
    p = pyaudio.PyAudio()
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True,
                    stream_callback=callback
                    )
    stream.start_stream()

    # play the audio in chunks
    while stream.is_active():
        time.sleep(0.1)

    # close everything
    stream.stop_stream()
    stream.close()
    p.terminate()

# Define some simple functions to aid in looking at the time/frequency domains of the speech.
def plot_time_domain(signal, fs, title_keyword):
    time_indices = np.arange(len(signal)) / float(fs)
    plt.plot(time_indices, signal)
    plt.title("Time Domain of {}".format(title_keyword))
    plt.xlabel("time (s)")
    plt.ylabel("amplitude")
    plt.show()

def plot_spectrogram(signal, fs, nfft, title_keyword):
    [S, freqs, bins, _] = plt.specgram(signal, NFFT=nfft, Fs=fs, window=np.hamming(nfft), pad_to=nfft)
    plt.title("Spectrogram of {}".format(title_keyword))
    plt.xlabel("Time (s)")
    plt.ylabel("Frequency (Hz)")
    plt.show()

def plot_dft(signal, fs, nfft, title_keyword):
    X = fft(signal, n=nfft)
    freqs = fftfreq(nfft) * fs
    plt.plot(freqs, abs(np.real(X)))
    plt.title("DFT Magnitude of {}".format(title_keyword))
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Magnitude")
    plt.show()

def observe_signal(signal, nfft=1024, fs=16000, title=""):
    plt.subplot(211)
    plot_time_domain(signal, fs, title)
    plt.subplot(212)
    plot_spectrogram(signal, fs, nfft, title)
