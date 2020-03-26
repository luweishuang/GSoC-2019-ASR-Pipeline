---
title: Week 9 Summary
date: 2019-08-31 23:00:00
tags:
- coding
---

<!-- toc -->

In this post, I'll summarize things I did in week 9.

We've finished training, testing and decoding on Chinese data. So from this week on, we'll focus on Red Hend Lab data and creating a portable pipeline.

<!-- more -->

The pipeline script is at https://github.com/qibinc/GSoC-2019-ASR-Pipeline/blob/master/infer.sh, based on last year's pipeline for DeepSpeech2. Since the wav2letter++ package differs much from Deepspeech2, many parts of the pipeline needs to be modified. For easy understanding, I divide this pipeline into 4 parts:

1. Locating and copying data
2. Converting mp4 to wav and split wav
3. Creating manifest file for wav2letter++
4. Run wav2letter++

In this post, we focus on part 1 – Locating and copying data

[These lines](https://github.com/qibinc/GSoC-2019-ASR-Pipeline/blob/76649a8b9a03496368da4fc4f712dbef6b02c4ca/infer.sh#L23-L38), written by Zhaoqing in 2018, resolve the argument `day N`, and assgin `DIR` to the directory for that day.

After that, we'll create `temp_data/` and `temp_manifest`. They store the temporal audio files and manifests, respectively.

```bash
rm -rf temp_data
rm -rf temp_manifest
mkdir -p $PWDDIR/temp_data/
mkdir -p $PWDDIR/temp_manifest/
```

Next, we'll copy all Chinese video files and their descriptions to our temporal directory `temp_data` because we don't have the permission to modify the original directory and it has many irrelevant files.

```bash
find . -name '*_CN_*.mp4' ! -iname "*CGTN*" -exec cp {} $PWDDIR/temp_data/ \;
find . -name '*_CN_*.txt' ! -iname "*CGTN*" -exec cp {} $PWDDIR/temp_data/ \;
```

These are basically what part 1 dooes. In the meanwhile, I compressed the pretrained model file and uploaded it to Dropbox so that the pipeline can download and use it.
