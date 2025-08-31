import os
import shutil
from math import ceil

# === CONFIG ===
source_folder = r"/root/data/genshin/reverb_train___"  # Folder containing files
files_per_folder = 100                                # Number of files per subfolder
prefix = "p_"                                     # Prefix for subfolder names

# === SCRIPT ===
# Get all files (ignore directories)
all_files = [f for f in os.listdir(source_folder) if os.path.isfile(os.path.join(source_folder, f))]
total_files = len(all_files)

if total_files == 0:
    print("No files found in the source folder.")
else:
    num_subfolders = ceil(total_files / files_per_folder)
    print(f"Found {total_files} files. Creating {num_subfolders} subfolders...")

    for i in range(num_subfolders):
        # Create subfolder name
        subfolder_name = f"{prefix}{i+1}"
        subfolder_path = os.path.join(source_folder, subfolder_name)
        os.makedirs(subfolder_path, exist_ok=True)

        # Get the slice of files for this subfolder
        start = i * files_per_folder
        end = start + files_per_folder
        batch_files = all_files[start:end]

        # Move files into the subfolder
        for file_name in batch_files:
            src_path = os.path.join(source_folder, file_name)
            dest_path = os.path.join(subfolder_path, file_name)
            shutil.move(src_path, dest_path)

    print("✅ Files have been separated into subfolders.")