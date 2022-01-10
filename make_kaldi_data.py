#!/usr/bin/env python3
import sys
import numpy as np
import warnings
from utils import *
warnings.filterwarnings('ignore')

if __name__ == '__main__':
    masterkey_path = sys.argv[1]
    audio_path = sys.argv[2]
    data_dir_path = sys.argv[3]
    languages = ['Tigrinya'] # change the language

    tasks = ["train", "test"]
    masterkey = np.loadtxt(masterkey_path, delimiter=";", dtype="object")
    language_filtered_key = filter_key(masterkey, languages)
    for task in tasks:
        mkdir_p(f"{data_dir_path}/{task}")
        task_filtered_key = filter_key(language_filtered_key, task=task)
        names, idxs = np.unique(task_filtered_key[:, 0], return_inverse=True)
        filtered_files = {n: task_filtered_key[idxs == ii] for ii, n in enumerate(names)}
        make_split(task, filtered_files, audio_path, data_dir_path)
    
    print_key_analysis(language_filtered_key)
    make_local_dict(data_dir_path, language_filtered_key[:, 5])
