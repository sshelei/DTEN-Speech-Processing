# DTEN Speech Processing

Python-based audio processing workflow developed during my internship at DTEN.

The project automates preprocessing and evaluation of speech recordings, including batch audio handling, loudness normalization, speech enhancement, and objective quality scoring.

## Features

- Batch-process WAV audio files across directories
- Normalize audio loudness
- Apply a pretrained speech-enhancement model to reduce background noise and reverberation
- Evaluate processed recordings using DNSMOS
- Export quality scores to CSV
- Generate JSON lists of recordings that fall below configurable quality thresholds

## Technologies

- Python
- librosa
- soundfile
- pyloudnorm
- MossFormer / ClearVoice
- DNSMOS

## Internship Work

During the internship, I:
- Prepared and standardized a dataset of roughly 1,000 audio recordings
- Converted external speech datasets into the required WAV format
- Added batch-processing support for speech enhancement
- Automated audio-quality evaluation and result export

## My Contributions
Pipeline Specific (`src/`)
- `clean_preprocess.py` — implemented batch audio preprocessing and integration
  of pretrained MossFormer speech enhancement
- `clean_filter.py` — automated DNSMOS evaluation and CSV/JSON result generation
- `audio_preprocess.py` — automated batch execution of audio preprocessing
- `info.py` — validated WAV files and dataset formatting
- `evaluate_files.py` - evaluate files based on chosen metrics

Helper (`helper_scripts/`) are intended for small steps like converting to WAV format, separating into subfolders, checking dataset formatting.

## Supporting Code

Some scripts in this repository named below were provided as
part of the existing internship project and were used to generate or prepare
audio for the processing workflow. They are in `provided/`
- `simulate_room.py` — provided room-simulation utility used to generate noisy test audio
- `download_dns.sh` — helper script to download audio files

## External Resources
- `download_ears.py` — helper script to download files used to train
      Downloaded from Meta's EARS Dataset repository (https://github.com/facebookresearch/ears_dataset.git)
  
## Purpose

The workflow was developed to reduce manual processing when preparing and evaluating speech recordings for speech-enhancement experiments.
