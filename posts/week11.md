---
title: Week 11 Summary
date: 2019-08-31 23:25:00
tags:
- coding
---

<!-- toc -->

In this post, I'll summarize things I did in week 11.

<!-- more -->

Recall the four parts:

1. ✅ Locating and copying data
2. ✅ Converting mp4 to wav and split wav
3. Creating manifest file for wav2letter++
4. Run wav2letter++

We'll focus on part 3 in this post. But do we need to create manifest files? Can we apply wav2letter++ directly on the .wav files?

We can't. As introduced in [this post](https://qibinc.github.io/blog/2019/06/17/wav2letter-md/), wav2letter++ needs some other files provided alongside the wav. Also, the filename should starts from `00000000`

I deal with these operations in `manifest.py`. In the pipeline, we only need to iterate over the audios and run `manifest.py` on them.

```bash
# Create manifests
for FIL in `ls -d $DAT*` ; do

   # Skip existing files
   if [ -f $PWDDIR'/new_text/'$YEAR/$MONTH/$DAT/${FIL%.*}.txt ] ; then echo -e "\tSkipping manifest for $FIL" ; continue ; fi

   python ../manifest.py \
     --target_dir=$PWDDIR/temp_data/$FIL  \
     --manifest_path=$PWDDIR/temp_manifest/$FIL
done
```
