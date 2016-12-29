# high-level imports
import numpy as np
from scipy.io.wavfile import read as wavread, write as wavwrite
from matplotlib import pyplot as plt
import pyaudio
import wave
from scipy import signal
from scipy.interpolate import interp1d
from numpy.fft import fft, fftfreq

# Opens the file and plays it via an output audio stream.
def play_audio(file_name):
    wf = wave.open(file_name, 'r')
    p = pyaudio.PyAudio()
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)

    # play the audio in chunks
    data = wf.readframes(512)
    while data != '':
        stream.write(data)
        data = wf.readframes(512)

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