---
title: Chinese ASR using wav2letter++ - Towards Training on Chinese data (Part 2)
date: 2019-06-24 18:31:00
tags:
- coding
---

<!-- toc -->

## Towards Training on Chinese data (Part 2)

> Note: before diving into this blog, it is suggested to read [this](https://qibinc.github.io/blog/2019/06/01/gsoc_singularity/) for the enviroment setup and [this](https://qibinc.github.io/blog/2019/06/10/wav2letter-english-md/) for a simpler demo.

In the last post, we introduced how to prepare Chinese data for wav2letter++ training. For the complete code for preprocessing the aishell dataset, you can refer to [this file](https://github.com/qibinc/GSoC-2019-ASR-Pipeline/blob/master/aishell/prepare_data.py). Now, let's have a look at the training for the Chinese dataset.

<!-- more -->

### Training

#### Model choices

Roughly, there are two main types of models for ASR based on deep learning. Sequence-to-sequence learning is proposed in around 2014 and RNNs (recurrent neural networks), e.g. LSTM, are applied to the seq2seq framework. Later, models fully based on convolutions, e.g. GCNN, are proved to be as effective as RNNs and are more efficient. In wav2letter++, both types of models are supported and here we'll try both of them out and choose the better one.
(Note: More recently, Transformers are proposed and demonstrate significant improvements over RNNs and CNNs, on the various language modeling tasks. However, there are few work applying Transformers to ASR task and wav2letter++ doesn't support Transformer either. Therefore, we only consider RNNs and CNNs here.)

#### Training configuration

##### Conv-based

For training a Conv-based model, we use the training specs as follows:

```bash
# Training config for Librispeech using Gated ConvNets
# Replace `[...]` with appropriate paths
--runname=aishell_conv_glu_trainlogs/
--datadir=aishell/
--tokensdir=aishell/
--rundir=.
--archdir=aishell/
--train=data/train
--valid=data/dev
--input=wav
--arch=network_conv_glu.arch
--tokens=data/tokens.txt
--criterion=asg
--lr=0.6
--lrcrit=0.006
--linseg=1
--momentum=0.8
--maxgradnorm=0.2
--replabel=2
--surround=|
--onorm=target
--sqnorm=true
--mfsc=true
--nthread=6
--batchsize=4
--transdiag=4
--iter=200
```

##### RNN-based

For training a conventional seq2seq model based on RNNs, use the training configuration as follows:

```bash
# Training config for Librispeech using Time-Depth Separable Convolutions
# Replace `[...]` with appropriate paths
--runname=seq2seq_tds_trainlogs/
--datadir=aishell/
--tokensdir=aishell/
--rundir=.
--archdir=aishell/
--train=data/train
--valid=data/dev
--input=wav
--arch=network_seq2seq_tds.arch
--tokens=data/tokens.txt
--criterion=seq2seq
--lr=0.05
--lrcrit=0.05
--momentum=0.0
--stepsize=40
--gamma=0.5
--maxgradnorm=15
--mfsc=true
--dataorder=output_spiral
--inputbinsize=25
--filterbanks=80
--attention=keyvalue
--encoderdim=512
--attnWindow=softPretrain
--softwstd=4
--trainWithWindow=true
--pretrainWindow=3
--maxdecoderoutputlen=120
--usewordpiece=true
--wordseparator=_
--sampletarget=0.01
--batchsize=16
--labelsmooth=0.05
--nthread=6
--memstepsize=4194304
--eostoken=true
--pcttraineval=1
--pctteacherforcing=99
--iter=200
```

#### Architecture specs

A really good wav2letter++ feature is that you don't have to change the source code for trying out different architectures. They made a specific format for defining architectures and building neural networks are as easy as drawing flow charts.

Here, we provide the network architecture file for training [Conv-based models](https://github.com/qibinc/GSoC-2019-ASR-Pipeline/blob/master/aishell/network_conv_glu.arch) and [RNN-based models](https://github.com/qibinc/GSoC-2019-ASR-Pipeline/blob/master/aishell/network_seq2seq_tds.arch).

#### Results

Currently the results are not satisfactory (actually kinda bad..) and it took so long to train a model on the Chinese corpus. We use the training and validation WER (Word Error Rate) as our evaluation metric. Results will be updated here:

|Model|WER-train|WER-dev|
|---|---|---|
|Conv-based|-|-|
|RNN-based|16.4|59.1|

As we can see, there is a huge gap between training and validation, which means either our model is overfitting or the dataset is too small. As the aishell dataset is commonly used, we suspect the model architecture used now is problematic. Also, we learned that architectures which work better for English may not work on Chinese data, as the two languages are quite different. (This has also been pointed out by other people whoe are trying to make wav2letter++ work on the aishell dataset [here](https://github.com/facebookresearch/wav2letter/issues/167)). Unfortunately, conv-based models are failing on aishell dataset and not producing any meaningful results, I'm still working on it.
