---
title: Chinese ASR using wav2letter++ - Towards Training on Chinese data (Part 3) Appendix
date: 2019-07-29 20:31:00
tags:
- coding
---

<!-- toc -->

## Towards Training on Chinese data (Part 3) Appendix

> Note: before diving into this blog, it is suggested to read [this](https://qibinc.github.io/blog/2019/06/01/gsoc_singularity/) for the enviroment setup and [this](https://qibinc.github.io/blog/2019/06/10/wav2letter-english-md/) for a simpler demo. And also [Part 1](https://qibinc.github.io/blog/2019/06/17/wav2letter-md/), [Part 2](https://qibinc.github.io/blog/2019/06/24/wav2letter-md-part-2/) and [Part 3](https://qibinc.github.io/blog/2019/07/23/wav2letter-md-part-3/).

In the last post, we generate texts directly using the seq2seq encoder and decoder. Wav2letter++ provides a way to improve the decoding phase — leveraging existing language models. These language models are commonly trained on much larger corpus and can help the ASR model generalize better by reweighting sentences in the beam search.

<!-- more -->

### Download LM

First, download a Chinese [KenLM](https://kheafield.com/code/kenlm/), which is one of the two types of LM that wav2letter++ supports (KenLM, ConvLM).

```bash
# LM provided by DeepSpeech
wget https://deepspeech.bj.bcebos.com/zh_lm/zh_giga.no_cna_cmn.prune01244.klm
```

### Decoding with LM

According to [wav2letter++ decoding documentation](https://github.com/facebookresearch/wav2letter/blob/master/docs/decoder.md#seq2seq--token-lm), we need a specific config file for decoding with LM.
For our implementation, see the decode config file [here](https://github.com/qibinc/GSoC-2019-ASR-Pipeline/blob/master/aishell/decode_seq2seq_tds.cfg). To run with this config, simply:

> Note: You may want to change the first line (`--am=seq2seq_tds_trainlogs/001_model_data#dev__backup.bin`) and the second line (`--lm=zh_giga.no_cna_cmn.prune01244.klm`) of the config file. `--am` and `--lm` points to the trained ASR model and the downloaded LM, respectively.

```bash
make decode
```

However, I found that there is some inconsistency between the vocabulary of the ASR model and the vocabulary of the LM, which causes the following problem:

```
F0729 14:57:30.904127  9274 Dictionary.cpp:51] Unknown token in dictionary: '_'
*** Check failure stack trace: ***
    @     0x7fee1538e5cd  google::LogMessage::Fail()
    @     0x7fee15390433  google::LogMessage::SendToLog()
    @     0x7fee1538e15b  google::LogMessage::Flush()
    @     0x7fee15390e1e  google::LogMessageFatal::~LogMessageFatal()
    @           0x50bf5a  w2l::Dictionary::getIndex()
    @           0x419a98  main
    @     0x7fedcc647830  __libc_start_main
    @           0x476389  _start
    @              (nil)  (unknown)
Makefile:15: recipe for target 'decode' failed
```

After some searching, I found this is because when preprocessing data for training the seq2seq model, wav2letter++ will prepend a `_` before every word for some reason. AFAIK, one solution to solve this is to change the wav2letter++ source code accordingly and recompile it. Another solution is to train a KenLM from scratch, using the same vocabulary as in the ASR model. Both of these solutions are dirty and not ideal. If you find out a better solution, please leave a comment below or email me, thank you!
