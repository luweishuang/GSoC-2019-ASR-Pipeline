---
title: Chinese ASR using wav2letter++ - Testing on English data
date: 2019-06-10 16:00:27
tags:
- coding
---

<!-- toc -->

## An example on applying wav2letter++ on English audio data

> Note: before diving into this blog, it is suggested to read [this](https://qibinc.github.io/blog/2019/06/01/gsoc_singularity/) for the enviroment setup.

### Data Preparation

- First, download the open-sourced Librispeech dataset.

```bash
W2LDIR=/home/$USER/w2l # or any other path where you want to keep the data
mkdir -p $W2LDIR
wget -qO- http://www.openslr.org/resources/12/train-clean-100.tar.gz | tar xvz -C $W2LDIR
wget -qO- http://www.openslr.org/resources/12/dev-clean.tar.gz | tar xvz -C $W2LDIR
wget -qO- http://www.openslr.org/resources/12/test-clean.tar.gz | tar xvz -C $W2LDIR
```

- Then, run preprocessing as following:

```bash
python wav2letter/tutorials/1-librispeech_clean/prepare_data.py --src $W2LDIR/LibriSpeech/ --dst $W2LDIR
python wav2letter/tutorials/1-librispeech_clean/prepare_lm.py --dst $W2LDIR
```

### Training

<!-- more -->

- Checkout the model config for this example here: `wav2letter/tutorials/1-librispeech_clean/network.arch`
- And checkout training config file here: `wav2letter/tutorials/1-librispeech_clean/train.cfg`.
- In the above two files, specific paths are need for the `[...]` placeholders.
- Then, start training by:

```bash
./wav2letter/build/Train train --flagsfile wav2letter/tutorials/1-librispeech_clean/train.cfg
```

### Decoding

- Similarly, for decoding, edit the `decode.cfg` file first and run:

```bash
./wav2letter/build/Decoder --flagsfile wav2letter/tutorials/1-librispeech_clean/decode.cfg
```

- The WER (Word Error Rate) score will be reported.

## Next steps

Apply to Chinese data!
