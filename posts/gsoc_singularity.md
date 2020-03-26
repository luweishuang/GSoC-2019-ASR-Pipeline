---
title: Chinese ASR using wav2letter++ - Environment Setup (Building wav2letter++)
date: 2019-06-01 17:00:00
tags:
- coding
---

<!-- toc -->

## Building a Singularity container for wav2letter++

Unlike DeepSpeech2, the wav2letter++ library is implemented in C++ and thus the installation is more sophisticated.

First, learn about the build requirements and dependencies [here](https://github.com/facebookresearch/wav2letter/blob/master/docs/installation.md#build-requirements). Then follow instructions on building wav2letter++ on Linux.

Since we require setting up everything in a Singularity container so that everything is easily portable, study the [Singularity Quick Start Page](https://www.sylabs.io/guides/2.5/user-guide/quick_start.html), which helps understanding how Singularity works and [Singularity Hub](https://github.com/singularityhub/singularityhub.github.io/wiki/Build-A-Container), which automatically builds Singularity images according to configurations hosted on github.

## A demo

Here is a demo for how to build a Singularity container that includes ANY packages we wants to install, without sudo privileges.

<!-- more -->

- Create a GitHub repo and create a Singularity configuration file like [Singularity.demo](https://github.com/qibinc/singularity_containers/blob/master/Singularity.demo)
- In this demo config file, we try to install the `sl` package, which isn't provided by the CWRU HPC. 

```bash
apt-get -y update
apt-get -y install sl
```

- For practical use, just add more required packages and more commands.

> Note that we don't have to add a `sudo` before these commands because we by default have su permission in Singularity configuration files.

- Then wait for Singularity Hub to build this. You can checkout the status in the Hub's panel [here](https://www.singularity-hub.org/collections/3084) for this example.

## Pull the image

- On the CWRU server, we first load singularity into our `$PATH`, then pull the demo container built above.

```bash
module load singularity/2.5.1
singularity pull shub://qibinc/singularity_containers:demo
```

- The image is saved to `./qibinc-singularity_containers-master-demo.simg`

## Run the image

```bash
singularity shell qibinc-singularity_containers-master-demo.simg
```

- Now we've launched and connected to this container. In this container, type in command `sl`. Recall that this is the package that doesn't exist on CWRU HPC and we have installed in this Singularity container.

```
                          (  ) (@@) ( )  (@)  ()    @@    O     @     O     @      O
                     (@@@)
                 (    )
              (@@@@)

            (   )
         ====        ________                ___________
     _D _|  |_______/        \__I_I_____===__|_________|
      |(_)---  |   H\________/ |   |        =|___ ___|      _________________
      /     |  |   H  |  |     |   |         ||_| |_||     _|                \_____A
     |      |  |   H  |__--------------------| [___] |   =|                        |
     | ________|___H__/__|_____/[][]~\_______|       |   -|                        |
     |/ |   |-----------I_____I [][] []  D   |=======|____|________________________|_
   __/ =| o |=-O=====O=====O=====O \ ____Y___________|__|__________________________|_
    |/-=|___|=    ||    ||    ||    |_____/~\___/          |_D__D__D_|  |_D__D__D_|
     \_/      \__/  \__/  \__/  \__/      \_/               \_/   \_/    \_/   \_/

```

- It works!

## Use the off-the-shelf image (DEPRECATED)

- Actually, the wav2letter++ community has provided a docker image that satisfies all the building requirements. 
- Besides, Singularity can pull and run Docker images as well.

```bash
singularity pull docker://wav2letter/wav2letter:cuda-latest
```

### UPDATE

- It appears in `wav2letter/wav2letter`, the library is installed at `/root/wav2letter`, which is not accessible in a Singularity container (see [this](https://singularity.lbl.gov/docs-docker#1-installation-to-root)).
Therefore, I built another container where the library is installed at `/home/wav2letter`.

```bash
singularity pull docker://chenqibin422/wav2letter
```

- And everything is set up!
