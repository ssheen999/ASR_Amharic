#!/usr/bin/env python3
import sys
import numpy as np
import warnings
from utils import *
warnings.filterwarnings('ignore')

if __name__ == '__main__':
    data_dir_path = sys.argv[1]
    text_path=f'{data_dir_path}/text'
    txt = read_text_file(text_path)
    make_local_dict(data_dir_path,txt)
