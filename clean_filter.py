import os
import sys
import csv
import json

# Replace with your own path to speechscore
os.chdir("/root/data/ClearerVoice-Studio/speechscore")

# Import the SpeechScore class to evaluate speech quality metrics
current_dir = os.path.dirname(os.path.realpath(__file__))
other_folder = os.path.join(current_dir, "ClearerVoice-Studio", "speechscore")
if other_folder not in sys.path:
    sys.path.insert(0, other_folder)
from speechscore import SpeechScore 

# generate csv file with scores
def generate_csv_file (test_path, file_name):
    mySpeechScore = SpeechScore([ 'DNSMOS' ])
    file = open(file_name, "w", newline='') 
    writer = csv.writer(file)
    headers = ["File Path", "BAK", "OVRL", "P808_MOS", "SIG"]
    writer.writerow(headers)
    for root, dirs, files in os.walk(test_path):
        audio_files = [f for f in files if f.endswith(".wav")]
        if audio_files:
            scores = mySpeechScore(test_path=root, reference_path=None, window=None, score_rate=16000)
            for filename in scores.keys():
                bak_scores = scores[filename]['DNSMOS']['BAK']
                ovrl_scores = scores[filename]['DNSMOS']['OVRL']
                p808_scores = scores[filename]['DNSMOS']['P808_MOS']
                sig_scores = scores[filename]['DNSMOS']['SIG']
                path = os.path.join(root, filename)
                field = [path, bak_scores, ovrl_scores, p808_scores, sig_scores]
                writer.writerow(field)
    file.close()

# generate json file of paths with scores corresponding to score_marker under threshold
def generate_json_file (csv_name, json_name, threshold, score_marker):
    csv_file = open(csv_name, "r") 
    csv_reader = csv.reader(csv_file, delimiter=',')
    header = next(csv_reader)
    json_file = open(json_name, "w")
    marker = {"threshold" : threshold, "marker" : score_marker}
    json.dump(marker, json_file, indent=4)
    match score_marker:
        case "BAK":
            for row in csv_reader:
                if (row[1] < threshold):
                    data = {row[0]: row[1]}
                    json.dump(data, json_file, indent=4)
        case "OVRL":
            for row in csv_reader:
                if (row[2] < threshold):
                    data = {row[0]: row[2]}
                    json.dump(data, json_file, indent=4)
        case "P808":
            for row in csv_reader:
                if (row[3] < threshold):
                    data = {row[0]: row[3]}
                    json.dump(data, json_file, indent=4)
        case "SIG":
            for row in csv_reader:
                if (row[4] < threshold):
                    data = {row[0]: row[4]}
                    json.dump(data, json_file, indent=4)
        case _:
            for row in csv_reader:
                if (row[1] < threshold):
                    data = {row[0]: row[1]}
                    json.dump(data, json_file, indent=4)
    csv_file.close()
    json_file.close()

# Main block 
if __name__ == '__main__':
    if len(sys.argv) <= 1:
        print("No arguments were provided.")
        sys.exit(1)
    
    # arguments 
    test_path = sys.argv[2] 
    # "/root/data/ears_v2/clean_train_processed"
    # "/root/data/ears_v2/clean_train_normalized"
    csv_name = "/root/data/ears_v2.csv"
    json_name = "/root/data/ears_v2.json"
    threshold = sys.argv[1]
    score_marker = sys.argv[3]

    # function calls
    generate_csv_file(test_path, csv_name)
    generate_json_file(csv_name, json_name, threshold, score_marker)
    