---
title: Chinese ASR using wav2letter++ - Towards Training on Chinese data (Part 1)
date: 2019-06-17 18:00:00
tags:
- coding
---

<!-- toc -->

## Towards Training on Chinese data (Part 1)

> Note: before diving into this blog, it is suggested to read [this](https://qibinc.github.io/blog/2019/06/01/gsoc_singularity/) for the enviroment setup and [this](https://qibinc.github.io/blog/2019/06/10/wav2letter-english-md/) for a simpler demo.

As wav2letter++ doesn't have an official and off-the-shelf support for the Chinese language, training a Chinese ASR model using wav2letter++ is non-trivial. Fortunately, wav2letter++ supports utf-8 encoding, which means it fundamentally supports all languages that have a vocabulary in utf-8 encoding. This blog will introduce how to train, test and tune a Chinese ASR model step by step. As the whole process is quite complex, I plan to split this into two to three blogs.

First, let's have a look at the data preparation for the Chinese dataset.

<!-- more -->

### Data Preparation

#### Dataset

The dataset from Red Hen (from Chinese News broadcast) is relatively small and doesn't contain the ground truth text, which means we can't either train or evaluate on it.
(NOTE: Ziyi has just kindly made a test set [here](https://liuziyi219.github.io/2019/06/16/Chinese-Pipeline-week3/) with great effort! We'll be able to evaluate on these data in the future.)

Therefore, we use the [aishell](http://www.openslr.org/33) dataset, the one DeepSpeech2 uses by default, containing 400 speakers and over 170 hours of Mandarin speech data. The unpreprocessed dataset can be download from [here](http://www.openslr.org/33).
(NOTE: In DeepSpeech2, the larger model is trained on a Baidu internal Mandarin dataset, containing over 1000 hours of speech data. The dataset seems not to be publicly available, which is very sad. A larger dataset will undoubtedly contribute to the quality of the trained model.)

The dataset can be simply understood as a bunch of (.wav, .txt) files, corresponding to the speech file and the annotated text. For simplicity, we don't perform VAD (Voice Activity Detection) for the moment.

#### Feeding into wav2letter++

Now, let's have a look at the data format that wav2letter++ requires. According to [this page](https://github.com/facebookresearch/wav2letter/blob/master/docs/data_prep.md), it needs the following four types of inputs:

- Audio and Transcriptions data
- Token dictionary
- Lexicon
- Language Model

##### Audio and Transcriptions data

So, instead of simply having (.wav, .txt) pairs, we need (.wav, .wrd, .tkn, .id) tuples. Let's have a look at examples of these files.

`example.wav`
This is actually the original wav files :)

`example.wrd`
Chinese words are composed of characters. This file contains a list fo words, separated by the space.
```
企业 依靠 技术 挖潜 增效 他 负责 全厂 产品质量 与 技术培训 成了 厂里 的 大忙人
```

`example.tkn`
This file derives from the .wrd file. It is a list of tokens for the wrd. For Chinese, it's insanely simply and straight-forward. Only note that the 'space' between words is represented by '|' now.
```
企 业 | 依 靠 | 技 术 | 挖 潜 | 增 效 | 他 | 负 责 | 全 厂 | 产 品 质 量 | 与 | 技 术 培 训 | 成 了 | 厂 里 | 的 | 大 忙 人 
```

`example.id`
This file contains the profile (e.g., gender) of the speaker and can be utilized by the model. The aishell dataset provides the gender of the speaker.
```
file_id 0
gender  M
speaker_id      3
```

After understanding what they look like, it's not difficult to write a script and create them from the original dataset!

##### Token dictionary

"A token dictionary file consists of a list of all subword units." For Chinese, it is a dictionary of all the Chinese characters that appear in the dataset..

```bash
|
我
爱
谷
歌
和
红
母
鸡
...
```

##### Lexicon

This file maps a word to a list of tokens that can be found in the token dictionary above. Let the example speak for itself:

```
谷歌 谷 歌
中国 中 国
编程之夏 编 程 之 夏
```

Now, the basic preparation is done. However, you may have a question here similar to mine:  All these files derive from the original ground truth text files in the dataset. Why don't they just include this preprocessing part in the library?

My guess is that although for Chinese (and English) this process is simple, there may exist languages where words and tokens have a more complex relationship and require different rules. But after this tedious pre-processing, they are all the same utf-8 `tokens` to the model now.

##### Language model

The final preparation is a language model. But why a pretrained language model helps the quality of speech recognition? To provide an intuition, recall when typing on your phone. The prompts above the keyboard effectively guess what you are about to say, which not only speed up your typing, but lower the probability of typos and wrong grammars as well, so it improves the quality of your typing. The actual mechanism is of course more complicated. For details, you can refer to the DeepSpeech2 paper or the wav2letter++ paper.

Fortunately, wav2letter++ supports KenLM, which DeepSpeech also supports. Therefore, we download this lm using [this](https://github.com/PaddlePaddle/DeepSpeech/blob/develop/models/lm/download_lm_ch.sh) script.
