import os
import random
import multiprocessing

import librosa
import numpy as np
import soundfile as sf
import pyloudnorm as pln
import pyroomacoustics as pra
from pyroomacoustics.directivities import (
    DirectionVector,
    HyperCardioid,
)
from tqdm import tqdm

random.seed(42)
np.random.seed(42)

ROOM_DIMENSIONS = [10.0, 7.0, 3.5]
HEIGHTS = [1.50, 1.55, 1.60, 1.65, 1.70, 1.75, 1.80, 1.85, 1.90, 1.95, 2.00]

MIC_LOCATION = [0.0, 3.5, 1.75]
SOURCE_LOCATIONS = []
if True:
    for x in np.arange(0.0, ROOM_DIMENSIONS[0], 0.5):
        for y in np.arange(0.0, ROOM_DIMENSIONS[1], 0.5):
            SOURCE_LOCATIONS.append([x, y, random.choice(HEIGHTS)])
if False:
    for x in np.arange(ROOM_DIMENSIONS[0] - 2.0, ROOM_DIMENSIONS[0], 0.5):
        for y in np.arange(0.0, ROOM_DIMENSIONS[1], 0.5):
            SOURCE_LOCATIONS.append([x, y, random.choice(HEIGHTS)])
AZIMUTHS = [0.0, 15.0, 30.0, 45.0, 60.0, 75.0, 90.0, 105.0, 120.0, 135.0, 150.0, 165.0, 180.0, 195.0, 210.0, 225.0, 240.0, 255.0, 270.0, 285.0, 300.0, 315.0, 330.0, 345.0]
COLATITUDES = [60.0, 75.0, 90.0, 105.0, 120.0]

def audionormalize(audio_data: np.ndarray, target_peak_amplitude: float = -3.0) -> np.ndarray:
    """
    Normalize the audio data to a target peak amplitude.

    Args:
        audio_data (numpy.ndarray): Audio data.
        target_peak_amplitude (float, optional): Target peak amplitude in dB. Defaults to -3.0.

    Returns:
        numpy.ndarray: Normalized audio data.
    """
    # Normalize the audio data to the target peak amplitude
    audio_data = pln.normalize.peak(audio_data, target_peak_amplitude)

    return audio_data

def process_file(
    clean_file_path : str,
    processed_clean_file_path : str,
    processed_reverb_file_path : str,
    processed_noise_file_path : str,
    noise_source_file_paths : list[str],
    room_dim : list[float],
    source_location : list[float],
    mic_location : list[float],
    azimuth : float,  # the angle of the source in the horizontal plane
    colatitude : float,  # the angle of the source in the vertical plane
    rt60 : float,  # seconds (the time it takes for the sound to decay by 60 dB)
    duration : float,  # output duration in seconds
    delay : float,  # noise delay in seconds
):
    # Inverting the Sabine formula to obtain the parameters for the ISM simulator
    e_absorption, max_order = pra.inverse_sabine(rt60, room_dim)

    # Create the room
    room = pra.ShoeBox(
        room_dim, fs=16000, materials=pra.Material(e_absorption), max_order=max_order,
        use_rand_ism=True, max_rand_disp=0.05,
        ray_tracing=False, air_absorption=True,
    )

    # Read the audio file
    clean_audio, fs = librosa.load(clean_file_path, sr=16000, duration=duration, offset=1.0)
    clean_audio = audionormalize(clean_audio, target_peak_amplitude=random.uniform(-6.0, -3.0))

    # Place the source in the room
    dir_obj = HyperCardioid(
        orientation=DirectionVector(azimuth=azimuth, colatitude=colatitude, degrees=True),
    )
    room.add_source(source_location, signal=clean_audio, directivity=dir_obj)

    # Place the microphone in the room
    room.add_microphone(mic_location)

    # Run the simulation
    room.simulate()

    # Align the signals
    reverb_audio = room.mic_array.signals[0]

    room.compute_rir()

    rir = room.rir[0][0]
    global_delay = pra.constants.get("frac_delay_length") // 2

    # Offset to skip the global delay padding
    search_start = global_delay
    search_rir = rir[search_start:]

    # Find the index of the first peak (or use threshold if needed)
    direct_index_local = np.argmax(np.abs(search_rir))
    direct_index_global = search_start + direct_index_local
    # -----

    # Create the room
    room = pra.ShoeBox(
        room_dim, fs=16000, materials=pra.Material(e_absorption), max_order=max_order,
        use_rand_ism=True, max_rand_disp=0.05,
        ray_tracing=False, air_absorption=True,
    )

    room.add_source(source_location, signal=clean_audio, directivity=dir_obj)

    # Place the microphone in the room
    room.add_microphone(mic_location)

    # Place the noise soures in the room
    assert len(noise_source_file_paths) == 4, "There should be 4 noise sources"
    for i in range(2):
        for j in range(2):
            noise_source_location = [room_dim[0] / 3 * (i + 1), room_dim[1] / 3 * (j + 1), random.uniform(0.0, room_dim[2])]

            noise_source_audio, _ = librosa.load(noise_source_file_paths[i * 2 + j], sr=16000, duration=duration - delay)
            noise_source_audio = audionormalize(noise_source_audio, target_peak_amplitude=random.uniform(-20.0, -15.0))

            room.add_source(noise_source_location, signal=noise_source_audio * 0.05, delay=delay)

    noise_source_location = [room_dim[0] / 2, room_dim[1] / 2, random.uniform(0.0, room_dim[2])]

    random_noise = np.random.randn(len(clean_audio) - int(delay * fs))
    random_noise = audionormalize(random_noise, target_peak_amplitude=random.uniform(-60.0, -55.0))

    room.add_source(noise_source_location, signal=random_noise, delay=delay)

    # Run the simulation
    room.simulate()

    # # Align the signals
    t_max = 1600
    noise_audio = room.mic_array.signals[0]
    # sample_delay = int(pra.sync.tdoa(clean_audio, noise_audio, fs=1, t_max=t_max, phat=True))
    sample_delay = -direct_index_global
    aligned_noise_audio = noise_audio[-sample_delay + int(delay * fs):]

    # sample_delay = int(pra.sync.tdoa(clean_audio, reverb_audio, fs=1, t_max=t_max, phat=True))
    sample_delay = -direct_index_global
    aligned_reverb_audio = reverb_audio[-sample_delay + int(delay * fs):]

    clean_audio = clean_audio[int(delay * fs):]
    aligned_noise_audio = aligned_noise_audio[:len(clean_audio)]
    aligned_reverb_audio = aligned_reverb_audio[:len(clean_audio)]

    if len(clean_audio) != len(aligned_noise_audio) or len(clean_audio) != len(aligned_reverb_audio):
        print(f"Audio files {clean_file_path} and {processed_noise_file_path} are not the same length.")
        return

    if len(clean_audio) < 32000:
        print(f"Audio file {clean_file_path} is less than 32000 samples.")
        return

    # # Verify the output
    # # print(f"Reference signal: {clean_audio.shape}")
    # # print(f"Aligned signal: {aligned_reverb_audio.shape}")
    # estimated_delay = np.argmax(np.correlate(clean_audio[:16000], aligned_reverb_audio[:16000], "full")) - (len(aligned_reverb_audio[:16000]) - 1)
    estimated_delay = int(pra.sync.tdoa(clean_audio, aligned_reverb_audio, fs=1, t_max=t_max, phat=True))
    if abs(estimated_delay) > 10:
        print(f"Estimated delay is too large: {estimated_delay}")
        return

    # # Save the audio files
    sf.write(processed_clean_file_path, clean_audio, fs)
    sf.write(processed_reverb_file_path, aligned_reverb_audio, fs)
    sf.write(processed_noise_file_path, aligned_noise_audio, fs)


# try catch wrapper for multiprocessing
def process_file_wrapper(args):
    try:
        process_file(*args)
    except Exception as e:
        print(f"Error processing {args[0]}: {e}")

if __name__ == "__main__":
    # CLEAN_FILE_DIR = "/root/data/genshin_v2/clean_train/"
    CLEAN_FILE_DIR = "/root/data/genshin/clean_train___/"
    # CLEAN_FILE_DIR = "/root/data/ears_v2/clean_train/"
    # CLEAN_FILE_DIR = "/root/speech_restoration/data/ears_v2/clean_train/" # this one was original
    # CLEAN_FILE_DIR = "/root/data/dns/datasets_fullband/clean_fullband/"

    noise_source_dir = "/root/data/dns/datasets_fullband/noise_fullband/"
    # noise_source_dir = "/root/speech_restoration/data/dns/datasets_fullband/noise_fullband"
    noise_source_files = os.listdir(noise_source_dir)

    # walk through the directory and subdirectories
    for root, dirs, files in os.walk(CLEAN_FILE_DIR):
        file_list = []
        dirs.sort()
        files.sort()

        print(f"Processing {root}")

        if not os.path.exists(root.replace("clean_train", "clean_train_processed")):
            os.makedirs(root.replace("clean_train", "clean_train_processed"))
        if not os.path.exists(root.replace("clean_test", "clean_test_processed")):
            os.makedirs(root.replace("clean_test", "clean_test_processed"))
        if not os.path.exists(root.replace("clean_train", "noise_train")):
            os.makedirs(root.replace("clean_train", "noise_train"))
        if not os.path.exists(root.replace("clean_test", "noise_test")):
            os.makedirs(root.replace("clean_test", "noise_test"))
        if not os.path.exists(root.replace("clean_train", "reverb_train")):
            os.makedirs(root.replace("clean_train", "reverb_train"))
        if not os.path.exists(root.replace("clean_test", "reverb_test")):
            os.makedirs(root.replace("clean_test", "reverb_test"))

        for file in files:
            if file.endswith(".wav") and file.find("whisper") == -1 and file.find("vegetative") == -1 and file.find("nonverbal") == -1:
                clean_file_path = os.path.join(root, file)
                processed_clean_file_path = clean_file_path.replace("clean_train", "clean_train_processed")
                processed_clean_file_path = processed_clean_file_path.replace("clean_test", "clean_test_processed")
                processed_reverb_file_path = clean_file_path.replace("clean_train", "reverb_train")
                processed_reverb_file_path = processed_reverb_file_path.replace("clean_test", "reverb_test")
                processed_noise_file_path = clean_file_path.replace("clean_train", "noise_train")
                processed_noise_file_path = processed_noise_file_path.replace("clean_test", "noise_test")

                selected_noise_source_files = random.sample(noise_source_files, 4)
                noise_source_file_paths = [os.path.join(noise_source_dir, noise_file) for noise_file in selected_noise_source_files]

                file_list.append((
                    clean_file_path,
                    processed_clean_file_path,
                    processed_reverb_file_path,
                    processed_noise_file_path,
                    noise_source_file_paths,
                    ROOM_DIMENSIONS,
                    random.choice(SOURCE_LOCATIONS),
                    MIC_LOCATION,
                    random.choice(AZIMUTHS),
                    random.choice(COLATITUDES),
                    0.5,
                    11.0,
                    1.0,
                ))

        num_workers = 30
        with multiprocessing.Pool(num_workers) as pool:
            list(tqdm(pool.imap(process_file_wrapper, file_list), total=len(file_list)))