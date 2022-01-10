#!/usr/bin/env bash


. ./path.sh
. ./cmd.sh


#DATA_DIR=./data
MODEL_DIR=./model_am
audio_file=example.wav


mkdir -p ${audio_file%.wav}
target_tmp=${audio_file%.wav}

DATA_DIR="${target_tmp}/data"
mkdir -p $DATA_DIR

mfccdir=${DATA_DIR}/mfcc/

sox $audio_file -c 1 -r 8000 -b 16 ${audio_file%.wav}_1.wav

audio_file=${audio_file%.wav}_1.wav
local/create-corpus.sh $DATA_DIR $audio_file

steps/make_mfcc.sh --mfcc-config $MODEL_DIR/conf/mfcc_hires80.conf --nj 1 --cmd "$train_cmd" \
  ${DATA_DIR} ${target_tmp}/exp/make_mfcc $mfccdir


steps/online/nnet2/extract_ivectors_online.sh --cmd "$train_cmd" --nj 1 \
      ${DATA_DIR} $MODEL_DIR/ivector_extractor \
      ${DATA_DIR}/ivectors_hires


ivector_period=$(cat ${DATA_DIR}/ivectors_hires/ivector_period)
ivector_opts="--online-ivectors=scp:${DATA_DIR}/ivectors_hires/ivector_online.1.scp --online-ivector-period=$ivector_period"

nnet3-latgen-faster $ivector_opts --frame-subsampling-factor=3 --frames-per-chunk=51 --extra-left-context=10 \
     --extra-right-context=0 --extra-left-context-initial=-1 --extra-right-context-final=-1 \
     --minimize=true --max-active=7000 --min-active=200 --beam=10.0 --lattice-beam=10.0 \
     --acoustic-scale=1.0 --allow-partial=true \
     --word-symbol-table=$MODEL_DIR/words.txt $MODEL_DIR/final.mdl $MODEL_DIR//HCLG.fst \
     "ark,s,cs:apply-cmvn --norm-means=false --norm-vars=false --utt2spk=ark:$DATA_DIR/utt2spk scp:$DATA_DIR/cmvn.scp scp:$DATA_DIR/feats.scp ark:- |" \
     "ark:|lattice-scale --acoustic-scale=0.85 ark:- ark:-  > $target_tmp/lat.1"

lattice-push ark:$target_tmp/lat.1 ark:$target_tmp/lat.2
lattice-to-ctm-conf --acoustic-scale=1.3 --frame-shift=0.03 --decode-mbr=true ark:$target_tmp/lat.2 $target_tmp/1.ctm
lattice-mbr-decode --acoustic-scale=1.3 ark:$target_tmp/lat.2 'ark,t:| utils/int2sym.pl -f 2- '$MODEL_DIR/words.txt' > text' ark:$target_tmp/1.text ark:$target_tmp/1.sau
  
