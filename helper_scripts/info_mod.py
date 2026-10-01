import os
import wave
import contextlib

folder_path = "/root/data/genshin_v2/clean_train/"  # Replace with your folder path of wav files

files = os.listdir(folder_path)
for i, file in enumerate(files):
    file_path = os.path.join(folder_path, file)
    with contextlib.closing(wave.open(file_path, 'rb')) as wf:
        n_channels = wf.getnchannels()
        sampwidth = wf.getsampwidth()
        framerate = wf.getframerate()
        # n_frames = wf.getnframes()
        # comptype = wf.getcomptype()
        # compname = wf.getcompname()
        # duration = n_frames / float(framerate)

        # collection of statements below: check the parameters of each sample are correct
        assert n_channels == 1, f"File {i}: Not 1 channel"
        assert sampwidth == 2, f"File {i}: Not 2 bytes"
        assert framerate == 16000, f"File {i}: Not 16,000 Hz"

        # collection of statements below: print statements
        # print(f"File {i}: {file_path}")
        # print(f"Channels: {n_channels}")
        # print(f"Sample Width (bytes): {sampwidth}")
        # print(f"Frame Rate (Hz): {framerate}")
        # print(f"Number of Frames: {n_frames}")
        # print(f"Compression Type: {comptype}")
        # print(f"Compression Name: {compname}")
        # print(f"Duration (seconds): {duration:.2f}")
