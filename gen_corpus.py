#! /usr/bin/env python3

import sys
import numpy as np
import warnings
from utils import *
warnings.filterwarnings('ignore')

def gen_corpus(text, text_path):
    corpus = []
    for s in text:
        raw_sentence = remove_harakat(s)
        clean_sentence = clean(raw_sentence)
        corpus.append(clean_sentence)
        text=corpus
    text = np.array(text)
    write_list(f"{text_path}/corpus.txt",text)

def read_corpus(file):
    text=[]
    with open(file) as f:
        lines = f.readlines()
        for line in lines:
            text.append(line)
        
    text = np.array(text)
        
    return text


def clean(sentences):
    sentences=sentences.replace("(())","<UNK>")
    #sentences=re.sub("\<.*\>", "<UNK>",sentences)
    words = sentences.split()
    new_sentences=''
    for w in words:
        word = w.replace("(())","<UNK>")
        word= word.replace(".","")
        word=re.sub("\<.*\>","<UNK>",word)
        if "-" in word:
            word="<UNK>"
        if "*" in word: 
            word="<UNK>"
        if "((" in word:
            word=word[2:]
        if "))" in word:
            word=word[:-2]
        if "%" in word:
            word="<UNK>"

        new_sentences+=word+" "

    return new_sentences


if __name__ == '__main__':
    text_path = sys.argv[1]
    text = read_corpus(f'{text_path}/corpus_old')
    gen_corpus(text,text_path)
    
