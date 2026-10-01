import os
import librosa
import numpy as np
import soundfile as sf
from datasets import load_dataset

output_dir = "/root/data/genshin_v2/clean_train___/"
ds = load_dataset("simon3000/genshin-voice", split = "train")
os.makedirs("/root/data/genshin_v2/clean_train___/")
#os.makedirs("/root/data/genshin_v2/clean_train___/Japanese")
#os.makedirs("/root/data/genshin_v2/clean_train___/Chinese")
#os.makedirs("/root/data/genshin_v2/clean_train___/Korean")
#os.makedirs("/root/data/genshin_v2/clean_train___/English(US)")
for i, file in enumerate(ds):
    y = file["audio"]["array"]
    sr = file["audio"]["sampling_rate"]
    language = file["language"]
    if (sr != 16000):
        y = librosa.resample(y, orig_sr=sr, target_sr=16000)
        sr = 16000
    y = librosa.to_mono(y)
    out_path = os.path.join(output_dir, f"audio{i}.wav")
    sf.write(out_path, y, 16000, "PCM_16")
   