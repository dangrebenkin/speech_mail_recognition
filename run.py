# coding:utf-8
import argparse
import configparser
import os
import re
import ast

import pandas as pd

# TODO: use as enviroment variables
KALDI_RU_PATH = '/audio_recognition/kaldi-ru/kaldi-ru-0.6'
os.environ['KALDI_ROOT'] = '/audio_recognition/kaldi/kaldi/'
CUR_PATH = os.path.split(os.path.abspath(__file__))[0]


def process_input(input_file, input_folder, log):
    input_files = []
    results = pd.DataFrame(columns=['filename', 'predicted'])

    if input_file is not None:
        filename = os.path.abspath(input_file)
        input_files.append(filename)

    if input_folder is not None:
        for file in os.listdir(input_folder):
            filename = os.path.join(input_folder, file)
            filename = os.path.abspath(filename)
            input_files.append(filename)

    config = configparser.ConfigParser()
    config.read('dictionary.cfg')

    dictionary = ast.literal_eval(config['PROCESS_SPEECH']['answerphone_dictionary'])

    os.chdir(KALDI_RU_PATH)
    for filename in input_files:
        is_answerphone = recognize_answerphone(filename, dictionary)
        results = results.append({
            'filename':  os.path.basename(filename),
            'predicted': int(is_answerphone),
        }, ignore_index=True)

        if log:
            print(filename)
            if is_answerphone:
                print('Распознанная запись - автоответчик')
            else:
                print('Распознанная запись - не автоответчик')
            print()
    os.chdir(CUR_PATH)

    return results


# TODO: hardcoded script execute, bad variables names
def recognize_answerphone(filename, dictionary):
    prea = './decode_file_python.sh' + ' ' + os.path.join(CUR_PATH, filename)
    a = os.popen(prea).read()
    pretext = re.findall(r'[а-я]\w+|[а-я]', a)
    text = ' '.join(pretext)

    for phrase in dictionary:
        pattern = re.search(phrase, text)
        if pattern is not None:
            return True

    return False


def calculate_metrics(predicted, labels):
    merged = predicted.join(labels.set_index('filename'), on='filename', how='left')
    wrong_results = merged[merged.label != merged.predicted]
    wrong_results = wrong_results.fillna({'label':'None'})
    if (len(merged) == 0):
        return 0, wrong_results
    accuracy = 1.0 - float(len(wrong_results)) / len(merged)
    return accuracy, wrong_results


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-r', '--recognition_one_file', dest='file_path', type=str,
                        help='input file path', required=False)
    parser.add_argument('-rd', '--recognition_directory_with_files', dest='folder_path', type=str,
                        help='folder with input files', required=False)
    parser.add_argument('--labels', dest='labels_path', type=str,
                        help='ground truth labels CSV dataset path. If passed, calculate metrics',
                        required=False)
    parser.add_argument('-log', '--stdout_log', dest='stdout_log', const=True, default=False,
                        help='print log to stdout', required=False, nargs='?')

    args = parser.parse_args()

    results = process_input(args.file_path, args.folder_path, args.stdout_log)
    results.to_csv('results', index=False)

    if args.labels_path is not None:
        labels = pd.read_csv(args.labels_path, header=None, index_col=False, names=['filename', 'label'])
        labels['label'].astype('int')
        accuracy, wrong_results = calculate_metrics(results, labels)
        if args.stdout_log:
            print('Accuracy: {0:.2%}'.format(accuracy))

        wrong_results.to_csv('wrongresults', index=False)
