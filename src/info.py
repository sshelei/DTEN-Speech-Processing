import wave
import contextlib

file_path = "/root/data/ears_v2/clean_train_processed/p016/sentences_18_regular.wav"  # Replace with your .wav file path

with contextlib.closing(wave.open(file_path, 'rb')) as wf:
    n_channels = wf.getnchannels()
    sampwidth = wf.getsampwidth()
    framerate = wf.getframerate()
    n_frames = wf.getnframes()
    comptype = wf.getcomptype()
    compname = wf.getcompname()
    duration = n_frames / float(framerate)

    assert n_channels == 1, "Not 1 channel"
    assert sampwidth == 2, "Not 2 bytes"
    assert framerate == 16000, "Not 16000 Hz"

    print(f"File: {file_path}")
    print(f"Channels: {n_channels}")
    print(f"Sample Width (bytes): {sampwidth}")
    print(f"Frame Rate (Hz): {framerate}")
    print(f"Number of Frames: {n_frames}")
    print(f"Compression Type: {comptype}")
    print(f"Compression Name: {compname}")
    print(f"Duration (seconds): {duration:.2f}")
