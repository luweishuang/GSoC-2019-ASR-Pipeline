---
title: Week 12 Summary
date: 2019-08-31 23:40:00
tags:
- coding
---

<!-- toc -->

In this post, I'll summarize things I did in week 12.

<!-- more -->

Recall the four parts introduced in [week 9](https://qibinc.github.io/blog/2019/08/31/week9/):

1. ✅ Locating and copying data
2. ✅ Converting mp4 to wav and split wav
3. ✅ Creating manifest file for wav2letter++
4. Run wav2letter++

Finally we have come to the last part. `infer.py` does most of the work. For the pipeline, we need to understand the arguments required by `infer.py` and iterate over all the audios as follows.

- `--input_file` specifies the input wav file description.
- `--output_file` specifies the path of generated text.
- `--infer_manifest` specifies the manifest file.

```bash
# Run the automated speech-to-text python script
for manifest in $DAT* ; do
	 echo -e "\n\tRunning ASR on $manifest ...\n"
         mkdir -p $PWDDIR'/new_text/'$YEAR/$MONTH/$DAT
         CUDA_VISIBLE_DEVICES=0 \
         python -u ../infer.py \
            --infer_manifest=$PWDDIR'/temp_manifest/'$manifest \
            --output_file=$PWDDIR'/new_text/'$YEAR/$MONTH/$DAT/$manifest'.txt' \
            --input_file=$PWDDIR'/temp_data/'$manifest'.txt'
            if [ $? -ne 0 ]; then
               echo "Failed in inference!"
               rm $PWDDIR'/new_text/'$YEAR/$MONTH/$DAT/$manifest'.txt'
               continue
            fi
            echo $manifest' is done'
            #rm $manifest
            #rm -rf $PWDDIR/temp_data/$manifest
done
```

Lastly, we'll remove the temporal data.

```bash
rm -rf $PWDDIR/temp_data/
rm -rf $PWDDIR/temp_manifest/
rm -rf $PWDDIR/aishell/temp_wav2letter/
rm ../output.txt
```

By now, the pipeline has finished, you should have a `new_text/` directory, which contains the generated texts.

Below I'll introduce `infer.py`.

Load manifest files, including file paths and other information.

```python
f = open(args.infer_manifest)
timelist = []
paths = []
for line in f:
    d = json.loads(line.strip())
    paths.append(d["audio_filepath"])
    timelist.append(d["duration"])
```

Extract meta information in the description file. This step is required because the output file should contains this information. (https://sites.google.com/site/distributedlittleredhen/home/the-cognitive-core-research-topics-in-red-hen/red-hen-data-format)

```python
with open(args.input_file, "rb") as f:
    l = f.readlines()
    l = [x.decode("utf-8") for x in l]
    l[8] = "ASR_01|CMN\n"
    start_time = l[0].split("|")[1]
    time_now = str(datetime.datetime.now())[:16]  # get the current time
    l[10] = "|".join(
        [
            "ASR_01",
            time_now,
            "Source_Program=Facebook wav2letter++,infer.sh",
            "Source_Person=Zhaoqing Xu,Ziyi Liu,Qibin Chen",
            "Codebook=Chinese Speech to Text\n",
        ]
    )
    end_line = ""
    if l[-1].startswith("END"):
        end_line = l[-1]
    l = l[:11]
```

Prepare files for wav2letter++ and run the decoding step.

```python
os.chdir("..")
if os.path.exists("aishell/temp_wav2letter"):
    shutil.rmtree("aishell/temp_wav2letter")
os.makedirs("aishell/temp_wav2letter", exist_ok=True)
for i, path in enumerate(paths):
    os.rename(path, f"aishell/temp_wav2letter/{i:09d}.wav")
    os.system(f"touch aishell/temp_wav2letter/{i:09d}.tkn")

os.system(
    "/home/wav2letter/build/Test --am=seq2seq_tds_trainlogs/001_model_data#dev__backup.bin --test=temp_wav2letter --maxload=-1 --show | tee output.txt"
)
```

Then, wav2letter++ will generate outputs using its own format. Let's parse it:

```python
results = []
ids = []
with open("output.txt", 'rb') as f:
    lines = f.readlines()
    assert len(lines) - 2 == len(paths) * 3
    for idx in range(len(paths)):
        out = lines[3 * idx + 1].decode('utf-8')
        out = out[4:].replace('|', '').replace(' ', '')
        sample = lines[3 * idx + 2].decode('utf-8')
        sample = int(sample[sample.find(':')+1:sample.find(',')])
        results.append(out.strip())
        ids.append(sample)
idxs = np.argsort(ids)
results = [results[idx] for idx in idxs]
```

Finally, we'll write the results in the Red Hen Lab format:

```python
time_format = "%Y%m%d%H%M%S.%f"
start_time += '.000'
for result, time in zip(results, timelist):
    with open(args.output_file, "ab+") as f:
        end = (
            datetime.datetime.strptime(start_time, time_format)
            + datetime.timedelta(0, time)
        ).strftime(time_format)
        prefix = start_time[0:18] + "|" + end[:-3] + "|ASR_01|"
        f.write(prefix.encode("utf-8"))
        f.write(result.encode("utf-8"))
        f.write("\n".encode("utf-8"))
        start_time = end
with open(args.output_file, "a+") as f:
    f.write(end_line)
```