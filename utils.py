import os
import errno
import numpy as np
import warnings
import re
warnings.filterwarnings('ignore')

def remove_unintelligible_word(word):
    word=word.replace("(())","<UNK>")
    word=re.sub("\(.*\)","",word)
    word=re.sub("\(","",word)
    word=word.replace("ضجة","")
    word=word.replace("تنفس","")
    return word

def remove_noises(word):
    word = word.replace("#lipsmack", "<UNK>")
    word = word.replace("#breath", "<UNK>")
    word = word.replace("#cough","<UNK>")
    word = word.replace("#click", "<UNK>")
    word = word.replace("#laugh","<UNK>")
    word = word.replace("#dtmf","<UNK>")
    word = word.replace("#noise","<UNK>")
    word = word.replace("#sta","<UNK>")
    word = re.sub("\[.*\]","<UNK>",word)
    return word
def remove_hesitance(word):
    word=word.replace("#ah","<UNK>")
    word=word.replace("#um","<UNK>")
    word=word.replace("#mhm","<UNK>")
    word=word.replace("#uhuh","<UNK>")
    return word
def clean_transcription(sentences):
    sentences = sentences.replace("(( ))", "<UNK>")
    words=sentences.split()
    new_sentences=''
    for i in words:
        word=remove_hesitance(i)
        word=remove_noises(word)
        word=remove_unintelligible_word(word)
        word=word.replace("%fp","<UNK>")
        word=word.replace("%pw","<UNK>")
        word=word.replace(".","")
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
    new_sentences=re.sub("\<.*\>","<UNK>",new_sentences)
    return new_sentences
def read_text_file(path):
    whole_data=np.loadtxt(path, dtype="object", delimiter=";")
    cleaned_data=[]
    for data in whole_data:
        # FIXME UGLY HACK DUE TO DATA
        cleaned_data.append(" ".join(data.split(" ")[1:-1]))
    return cleaned_data
def make_split(task, files, audio_path, data_dir_path,r_harakat=True):
    wavscp = []
    utt2spk = []
    text = []
    segments = []
    recordfile=[]
    for file, datas in files.items():
        wavscp.append([datas[0][0].replace("-", ""), audio_path + datas[0][1]])
        for data in datas:
            if r_harakat:
                new_sentence=remove_harakat(data[5])
            else:
                new_sentence=data[5]
            if len(new_sentence)>=5:
                s, e = extend_segment(data[3], data[4])
                sid = data[0].replace("-", "") + "_" + chr(int(data[2])+ord('A')) + "_" + str(
                    int(s * 10e7)) + "_" + str(int(e * 10e7))
                spk = data[0].replace("-", "") + "_" + chr(int(data[2])+ord('A'))
                segments.append([sid, data[0].replace("-", ""), s, e])
                utt2spk.append([sid, spk])
                text.append([sid, new_sentence])
    for i in wavscp:
        recordfile.append([i[0],i[0],"A"])
    np.savetxt(f"{data_dir_path}/{task}/segments", segments, delimiter=" ", fmt="%s")
    np.savetxt(f"{data_dir_path}/{task}/utt2spk", utt2spk, delimiter=" ", fmt="%s")
    np.savetxt(f"{data_dir_path}/{task}/text", text, delimiter=" ", fmt="%s")
    np.savetxt(f"{data_dir_path}/{task}/wav.scp", wavscp, delimiter=" ", fmt="%s")
    np.savetxt(f"{data_dir_path}/{task}/reco2file_and _channel", recordfile, delimiter=" ", fmt="%s")

def print_counts(data, text=""):
    total = len(data)
    classes, counts = np.unique(data, return_counts=True)
    print(text)
    for s,c in zip(classes, counts):
        print (f"{s}: {c} %.2f%%"%(c/total*100))
def print_stats(data, text=""):
    dta = np.array(data).astype(np.float)
    median = np.median(dta)
    mean = np.mean(dta)
    mi = np.min(dta)
    mx = np.max(dta)
    print (f"{text} %.2f, %.2f, %.2f, %.2f"%(mi, median, mean, mx))
def print_key_analysis(key):
    print_counts(key[:,8], "Genders")
    print_counts(key[:,7], "Sources")
    print_counts(key[:, 6], "Languages")
    print_stats(key[:,4].astype(np.float)-key[:,3].astype(np.float), "Sentence lengths (s):")

def filter_key(masterkey, languages=None, task=None, return_empty=False):
    newkey = masterkey
    if not return_empty:
        newkey = newkey[newkey[:, 0] != '0']
    #filter out languages
    if languages:
        newkey = newkey[[l in languages for l in newkey[:, 9]]]
    if task:
        # filter out tasks
        newkey = newkey[[get_filelist_type(fn) == task for fn in newkey[:, 0]]]
    return newkey
def make_ereplacements(word,esearch):
    if word[-5:] in esearch.keys():
        words=word.split()[0][:-5]+esearch[word[-5:]]
        return words
    else:
        return word
def make_freplacements(word,fsearch):
    if word[:5] in fsearch.keys():
        words=fsearch[word[:5]]+word.split()[0][5:]
        return words
    else:
        return word
def remove_harakat(raw_sentence):
    end_search = {'x0629': 'x0647'}
    first_search = {'x0623': 'x0627', 'x0622': 'x0627', 'x0624': 'x0627'}
    new_sentence=''
    for raw_word in raw_sentence.split():
        new_word = make_freplacements(raw_word, first_search)
        new_word = make_ereplacements(new_word, end_search)
        new_sentence += new_word + " "
    return new_sentence

def make_local_dict(path,text,extra_data=None,r_harakat=True):
    if r_harakat:
        t=[]
        for raw_sentence in text:
            t.append(remove_harakat(raw_sentence))
        text=t
    text = np.asarray(text)
    if extra_data is not None:
        extra_texts=open(extra_data,"r").readlines()
        extra_text_cleaned=[]
        for extra_text in extra_texts:
            extra_text_cleaned.append(remove_harakat(extra_text.replace("\n","")))
        extra_text_cleaned=np.asarray(extra_text_cleaned)
        text=np.concatenate((text,extra_text_cleaned))
    silence = ['<UNK>', 'sil']
    extra_question = []
    optional_silence = ['sil', ]
    lexicon, phones = make_lexicon(text, silence, optional_silence)
    dict_dir = f"{path}/local/dict"
    mkdir_p(dict_dir)
    np.savetxt(f"{dict_dir}/lexicon.txt", lexicon, fmt="%s")
    write_list(f"{dict_dir}/silence_phones.txt", silence)
    write_list(f"{dict_dir}/nonsilence_phones.txt", phones)
    write_list(f"{dict_dir}/extra_questions.txt", extra_question)
    write_list(f"{dict_dir}/optional_silence.txt", optional_silence)

def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise

def get_filelist_type(fn):
    if fn[0] in ['a','b','c','d']:
        return "test"
    else:
        return "train"
def write_list(f, lst):
    with open(f, "w") as fp:
        for l in lst:
            fp.write(f"{l}\n")


def convert_word_human(sentences):
    xwords=sentences.split()
    new_sentence=''
    for word in xwords:
        words=word.split('x')
        xword=''
        for i in words:
            if len(i)>1:
                xword+=chr(int(i,16))
        new_sentence+=xword+" "
    return new_sentence
arabic_words={}
arabic_invert={}
#f=open("/home/ricky/Documents/arabic_levant/levant_code/mappings.txt").readlines()
#for i in f:
#    arabic_words[i.split()[0]]=i.split()[1]
#    arabic_invert[i.split()[1]]=i.split()[0]

def convert_unicode_specified(word):
    words=word.split()
    new_sentences=''
    for word in words:
        for alpha in word:
            if word not in "<UNK>":
                if alpha in arabic_words.keys():
                    new_sentences+=arabic_words[alpha]
            else:
                new_sentences += alpha
        new_sentences += ' '
    return new_sentences[:-1]

def convert_unicode(word):
    words=word.split()
    new_sentences=''
    for word in words:
        for alpha in word:
            if word not in "<UNK>":
                new_sentences+= 'x%04x' % ord(alpha)
            else:
                new_sentences+=alpha
        new_sentences+=' '
    return new_sentences[:-1]
def make_lexicon(text, silence, optional_silence):
    phones = []
    raw_words = set(np.concatenate([sentence.split() for sentence in text]))
    non_phonemes = set(silence+optional_silence)
    lexicon = []
    for nonp in non_phonemes:
        lexicon.append([nonp, nonp])
    for word in raw_words:
        if word not in non_phonemes:
            start = "".join(i for i in word)
            end = " ".join("x" + i for i in word.split("x"))[1:]
            phones += end.split()
            lexicon.append([start, end])
    phonemes_new = [ph for ph in np.unique(phones) if ph not in non_phonemes]
    print(f"Number of sentences in set: {len(text)}")
    print(f"Number of words in set: {len(lexicon)}")
    print(f"Number of phonemes in set: {len(phonemes_new)}")
    return lexicon, phonemes_new

def extend_segment(start, end, ext=0.15):
    if float(start) - ext < 0:
        s = 0
    else:
        s = float(start) - ext
    if float(end) + ext < 0:
        e = 0
    else:
        e = float(end) + ext
    return s, e
