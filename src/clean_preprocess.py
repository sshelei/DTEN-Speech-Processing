import os
import librosa
import sys
import numpy as np
import pyloudnorm as pln
import soundfile as sf
from clearvoice import ClearVoice

def audionormalize(audio_data: np.ndarray, rate:float, lufs: float) -> np.ndarray:
    # Normalize the audio data to the target peak amplitude
    # audio_data = pln.normalize.peak(audio_data, target_peak_amplitude)

    # measure the loudness first 
    meter = pln.Meter(rate) # create meter
    loudness = meter.integrated_loudness(audio_data)
   
    # loudness normalize audio to dB LUFS
    audio_data = pln.normalize.loudness(audio_data, loudness, lufs)
    return audio_data

def speech_enhancement(input_dir, output_dir, lufs):
    os.makedirs(output_dir, exist_ok=True)
    for root, dirs, files in os.walk(input_dir):
        audio_files = [f for f in files if f.endswith(".wav")]
        if audio_files:
            for audio in audio_files:
                file_path = os.path.join(root, audio)
                clean_audio, fs = librosa.load(file_path, sr=16000, offset=1.0)
                clean_audio = audionormalize(clean_audio, 16000, lufs)
                myClearVoice = ClearVoice(task='speech_enhancement', model_names=['MossFormerGAN_SE_16K'])
                myClearVoice(input_path=file_path, online_write=True, output_path=output_dir)

if __name__ == "__main__":
    if len(sys.argv) <= 1:
        print("No arguments were provided.")
        sys.exit(1)

    # arguments
    lufs = float(sys.argv[1])
    input_dir = sys.argv[2] 
    #"/root/data/genshin_v2/clean_train_processed/"
    #"/root/data/ears_v2/clean_train_processed/"
    output_dir = "/root/data/ears_v2/clean_train_normalized"
    #"/root/data/genshin_v2/clean_train_normalized/"

    # function calls
    speech_enhancement(input_dir, output_dir, lufs)
   