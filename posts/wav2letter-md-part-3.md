---
title: Chinese ASR using wav2letter++ - Towards Training on Chinese data (Part 3)
date: 2019-07-23 00:31:00
tags:
- coding
---

<!-- toc -->

## Towards Training on Chinese data (Part 3)

> Note: before diving into this blog, it is suggested to read [this](https://qibinc.github.io/blog/2019/06/01/gsoc_singularity/) for the enviroment setup and [this](https://qibinc.github.io/blog/2019/06/10/wav2letter-english-md/) for a simpler demo. And also [Part 1](https://qibinc.github.io/blog/2019/06/17/wav2letter-md/) and [Part 2](https://qibinc.github.io/blog/2019/06/24/wav2letter-md-part-2/).

In this post, I'll introduce test scores and examples of the current best-performing model based on wav2letter++. **An important thing to note is that this model (LER 8.8%) outperforms last year's DeepSpeech2 model (LER 10.2% [ref](https://github.com/CynthiaSuwi/ASR-for-Chinese-Pipeline#3-demo)) on the same aishell dataset.**

<!-- more -->

### Testing

```bash
/home/wav2letter/build/Test  \
--am=seq2seq_tds_trainlogs/001_model_data#dev__backup.bin \
--test=data/test \
--maxload=-1 \
--show
```

#### Scores

It turns out that the wav2letter++ library might have some problems when computing WER (Word Error Rate) on the Chinese language. Here we report another metric LER (Letter Error Rate):
(For readers not familiar with Chinese, the *letter* here refers to Chinese characters, e.g., "谷", "歌" while a *word* is composed of one or more Chinese characters, e.g., "谷歌")

| Model   | WER-test | LER-test |
| ------- | -------- | -------- |
| Seq2seq | 60.7%    | 8.8%     |

As you can see, there is a huge divergence between the two metrics, which is not reasonable at all. Therefore, let's have a look at the generated examples and find out!

#### Examples

I **randomly** choose 10 examples from the test set and present the ground truth text and the generated results as follows:

<audio controls src="000001318.wav"> Your browser does not support the <code>audio</code> element.</audio>
|T|: 京 华 | 时 报 | 讯 | 记 者 | 武 红 | 利 | 与 | 家 人 | 来 京 | 旅 游
|P|: 京 华 | 时 报 | 讯 | 记 者 | 武 红 | 利 | 与 | 家 人 | 来 京 | 旅 游
[sample: 1318, WER: 0%, LER: 0%, total WER: 60.7532%, total LER: 8.78003%, progress: 14.0468%]

<audio controls src="000001426.wav"> Your browser does not support the <code>audio</code> element.</audio>
|T|: 在 | 冈 山 | 的 | 桃 | 太 郎 | 体 育 | 馆
|P|: 在 | 冈 山 | 的 | 淘 汰 | 能 | 体 育 | 馆
[sample: 1426, WER: 100%, LER: 25%, total WER: 60.7921%, total LER: 8.79155%, progress: 14.0608%]

<audio controls src="000001269.wav"> Your browser does not support the <code>audio</code> element.</audio>
|T|: 凡 | 依 法 | 应 当 | 进 行 | 环 评 | 的 | 建 设 | 规 划 | 和 | 项 目
|P|: 反 依 | 法 | 应 当 | 进 行 | 环 评 | 的 | 建 设 | 规 划 | 和 | 项 目
[sample: 1269, WER: 100%, LER: 11.5385%, total WER: 60.8309%, total LER: 8.79472%, progress: 14.0747%]

<audio controls src="000006444.wav"> Your browser does not support the <code>audio</code> element.</audio>
|T|: 达 到 | 保 护 | 心 脏 | 的 | 作 用
|P|: 达 到 | 保 护 | 心 脏 | 的 | 作 用
[sample: 6444, WER: 0%, LER: 0%, total WER: 60.7708%, total LER: 8.78965%, progress: 14.0886%]

<audio controls src="000006604.wav"> Your browser does not support the <code>audio</code> element.</audio>
|T|: 二 零 一 五 | 年 | 世 界 | 田 径 | 锦 标 | 赛 | 即 将 | 在 | 北 京 | 拉 开 | 序 幕
|P|: 二 零 一 五 | 年 | 世 界 | 田 径 | 锦 标 | 赛 | 季 间 | 在 | 北 京 | 拉 开 | 戏 幕
[sample: 6604, WER: 100%, LER: 9.67742%, total WER: 60.8095%, total LER: 8.79087%, progress: 14.1026%]

<audio controls src="000000588.wav"> Your browser does not support the <code>audio</code> element.</audio>
|T|: 杀 人 | 犯 | 受 | 民 警 | 感 召 | 行 刑 | 前 | 捐 | 器 官 | 谢 罪
|P|: 杀 人 | 贩 售 | 民 警 | 赶 | 招 | 行 行 | 前 | 捐 赠 | 关 | 谢 罪
[sample: 588, WER: 100%, LER: 40%, total WER: 60.8481%, total LER: 8.82535%, progress: 14.1165%]

<audio controls src="000007025.wav"> Your browser does not support the <code>audio</code> element.</audio>
|T|: 让 | 体 重 | 维 持 | 在 | 四 十 五 | 公 斤 | 左 右
|P|: 让 | 体 重 | 维 持 | 在 | 四 十 五 | 公 斤 | 左 右
[sample: 7025, WER: 0%, LER: 0%, total WER: 60.7882%, total LER: 8.81794%, progress: 14.1304%]

<audio controls src="000004956.wav"> Your browser does not support the <code>audio</code> element.</audio>
|T|: 引 导 | 社 会 | 资 本 | 投 入 | 农 业
|P|: 引 导 | 社 会 | 资 本 | 投 入 | 农 业
[sample: 4956, WER: 0%, LER: 0%, total WER: 60.7283%, total LER: 8.8125%, progress: 14.1444%]

<audio controls src="000003204.wav"> Your browser does not support the <code>audio</code> element.</audio>
|T|: 参 考 | 消 息 | 网 | 九 月 | 二 五 | 日 报 | 道 新 | 报 称
|P|: 参 考 | 消 息 | 网 | 九 月 | 二 五 | 日 报 | 道 新 | 报 | 称
[sample: 3204, WER: 100%, LER: 4.54545%, total WER: 60.767%, total LER: 8.80836%, progress: 14.1583%]

<audio controls src="000005102.wav"> Your browser does not support the <code>audio</code> element.</audio>
|T|: 盘 活 | 各 地 | 公 积 金 | 资 源
|P|: 盘 活 | 各 地 | 公 积 金 | 资 源
[sample: 5102, WER: 0%, LER: 0%, total WER: 60.7073%, total LER: 8.8037%, progress: 14.1722%]

As we can see from the examples, the reported LER accurately captures the ASR performance, while the WER is either 0% or 100%, which has some errors. Overall, the performance is quite good. In the next post, we'll train the model on a larger dataset and test on audios provided by Red Hen.
