---
title: Week 10 Summary
date: 2019-08-31 23:12:00
tags:
- coding
---

<!-- toc -->

In this post, I'll summarize things I did in week 10.

<!-- more -->

Recall the four parts:

1. ✅ Locating and copying data
2. Converting mp4 to wav and split wav
3. Creating manifest file for wav2letter++
4. Run wav2letter++

We'll focus on part 2 in this post.

First, iterate over the .mp4 files:

```bash
n=0 m=0
for FIL in $DAT*.mp4 ; do n=$[n+1]
```

Then, let's study the ffmpeg manual and convert the mp4 to wav:

```bash
n=0 m=0
for FIL in $DAT*.mp4 ; do n=$[n+1]
  ffmpeg -i $FIL -ac 1 -ar 16000 ${FIL%%.*}.wav
```

**Important Note: ** Make sure the sample rate (16000) is the same as the training data and is supported by the ASR library. For wav2letter++, 16000 is supported and is used in the aishell dataset.

By now, we have .wav files corresponding to their .mp4 files. Note that the wav files are a lot smaller since they only contain audio.

Next, we'll use the VAD (Voice Activity Detection) script to detect speech in .wav files and split them into shorter pieces.

```bash
for FIL in $DAT*.mp4 ; do n=$[n+1]

  # Skip existing files
#  if [ -f "$PWDDIR/new_text/$YEAR/$MONTH/$DAT/${FIL%.*}.txt" ] ; then echo -e "\t${FIL%.*}.txt has already been processed" ; m=$[m+1] ; continue ; fi

  # Extract and split the a16000 {FIL%%.*}.wav
  ffmpeg -i $FIL -ac 1 -ar 16000 ${FIL%%.*}.wav
  mkdir -p ${FIL%%.*}
  # Use VAD to split the whole audio into piece
  python ../audiosplit.py \
    --target_dir=$PWDDIR/temp_data/${FIL%%.*}.wav \
    --output_dir=$PWDDIR/temp_data/${FIL%%.*}
  
  rm ${FIL%%.*}.wav
  # rm $FIL

  # For all the pieces that are longer than 30 seconds, split them again
  python ../audiosplit.py \
    --target_dir=$PWDDIR/temp_data/${FIL%%.*}  --output_dir=$PWDDIR/temp_data/${FIL%%.*}
  echo $FIL' split completed' 
done
```

For now, we have pieces of audios that contain speech. You can comment out all the `rm` commands in the script adn listen to them and observe how they are cut. It's recommended to study `audiosplit.py` and try improve it.
