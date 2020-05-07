import numpy as np
import sounddevice as sd

sd.default.samplerate = 44100


def play_signal(time: float = 0.2, frequency: int = 550):
    # Generate time of samples between 0 and two seconds
    samples = np.arange(44100 * time) / 44100.0
    # Recall that a sinusoidal wave of frequency f has formula w(t) = A*sin(2*pi*f*t)
    wave = 10000 * np.sin(2 * np.pi * frequency * samples)
    # Convert it to wav format (16 bits)
    wav_wave = np.array(wave, dtype=np.int16)

    sd.play(wav_wave, blocking=True)
