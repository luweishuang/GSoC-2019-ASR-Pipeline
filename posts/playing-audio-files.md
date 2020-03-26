---
title: Playing audio and video files on remote servers more easily
date: 2019-06-04 19:40:00
tags:
- coding
---

<!-- toc -->

## The problem

As most of the data being processed in Red Hen Lab are multimedia.
Some of my peers feel that viewing these data is troublesome.
One obvious solution is to download these data to a local machine of course.
However, we only need to peek into these files and downloading the whole audio / video is very inefficient and wasteful, as we're generating processed audios / videos all the time during experiments.
A more economic way is to use techniques like streaming.

<!-- more -->

## Solution 1

1. Open a http server on HPC
1. Play on Chrome

```bash
python -m SimpleHTTPServer <port>
# In Chrome, open rider.case.edu:<port>
```

## Solution 2

1. Mount the remote disk to local machine

```bash
# Mount
sshfs <user>@<server-ip>:<remote_path> <local_path>
# Unmount
umount <local_path>
```

## Solution 3

1. Sync the remote files to local machine

```bash
rsync -avx --progress <user>@<server-ip>:<remote_path> <local_path>
```
