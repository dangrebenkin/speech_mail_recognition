# Speech mail recognition

## Installing:
1. Download the latest version of kaldi-ru.
2. Download Kaldi and install from https://github.com/kaldi-asr/kaldi.
3. Change paths KALDI_ROOT and KALDI_RU_PATH in run.py.

## Start: 

    python3 run.py [-h] [-r FILE_PATH] [-rd FOLDER_PATH] [--labels LABELS_PATH]
              [-log [STDOUT_LOG]]

It recognizes file FILE_PATH and all files from FOLDER_PATH, and (if you need) it compares predicted values with valus from file LABELS_PATH.

### Arguments

#### -r FILE_PATH
Optionally.

Path to .wav file for recognition.

#### -rd FOLDER_PATH
Optionally.

Path to the folder with many .wav files for recognition.

#### --labels LABELS_PATH
Optionally.

Path to CSV file with labels.

File format: without heading.

Colons: file name, value: 1 - voice mail, 0 - not voice mail.

#### -log [STDOUT_LOG]
Optionally.

Concludes the information of recognition to stdout.

### Example:

    python3 run.py -rd audio/ --labels Etalon2.csv -log
