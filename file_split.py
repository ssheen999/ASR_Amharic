#!/usr/bin/python3



import os
import shutil
import sys

#import glob

src_dir_path = "/raid/target/audio"
#to_dir_path = "/home/xun.wang/data_split/Amharic/audio"

to_dir_path = sys.argv[1]
#key = open("Amharic/key_Amharic","r").readlines()
# in the list, the file name after with \n, so we have to remove '\n'
#key = f.split("\n")
#key = [line.rstrip() for line in open('Amharic/key_Amharic')]
key = [line.rstrip() for line in open(sys.argv[2])]



if os.path.exists(src_dir_path):
    print("src_dir_path exists")

    for file in os.listdir(src_dir_path):
        for k in key:
            if k in file:
                print('Copy to ' + to_dir_path + file)
                shutil.copy(src_dir_path + '/' + file, to_dir_path +'/'+file)









#    dirs = os.listdir(src_dir_path)
#    files = glob.glob(os.path.join(src_dir_path + "/*.wav_0.wav"))
#    fname = []
#    for f in files:
#        f = os.path.basename(files)
#        fname.append(f)

#    for i in fname:
#        if i in key: 
#            shutil.cpoy(scr_dir_path + '/' + i, to_dir_path +'/'+ i)

#    for file in files:
#        fname = os.path.basename(file)
#        if fname in key:
#            shutil.cpoy(scr_dir_path + '/' + file, to_dir_path +'/'+file)



#    for file in os.listdir(src_dir_path):
#        fname = os.path.basename(file)
#        if fname in key:
#            shutil.cpoy(scr_dir_path + '/' + file, to_dir_path +'/'+file)

#        if os.path.isfile(src_dir_path+'/'+file):
#            for k in key:
#                if k in file:
#                    print('Copy to' + to_dir_path + file)
#                    shutil.copy(scr_dir_path + '/' + file, to_dir_path +'/'+file)
            #if key in file:
             #   print('Copy to ' + to_dir_path + file)
              #  shutil.copy(scr_dir_path + '/' + file, to_dir_path +'/'+file)



