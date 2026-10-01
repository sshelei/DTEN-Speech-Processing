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

## Repository Structure

- `clean_preprocess.py` — audio preprocessing and speech enhancement
- `clean_filter.py` — DNSMOS evaluation and quality filtering
- `audio_preprocess.py` — batch audio processing utilities
- `info.py` — WAV format validation

## Purpose

The workflow was developed to reduce manual processing when preparing and evaluating speech recordings for speech-enhancement experiments.
