---
title: Splitting audio files using VAD (Voice Activity Detection) tools
date: 2019-06-07 14:53:04
tags:
- coding
---

<!-- toc -->

## Why we need VAD

- Last year, the DeepSpeech2 pipeline simply split audios into 10-second pieces, which causes truncation of complete sentences.
- As suggested by Red Hen Lab mentors, we can detect voices in audio and split them based on sentences.

## Tools for VAD

<!-- more -->

- After an investigation, we choose [py-webrtcvad](https://github.com/wiseman/py-webrtcvad), which is based on the commonly used webrtcvad and has a python interface.

## Pseudo code

TODO
