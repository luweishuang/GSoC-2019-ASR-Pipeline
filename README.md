# GSoC-2019-ASR-Pipeline

## [Blog](https://qibinc.github.io/blog/)

Google Summer of Code 2019 Project: Chinese ASR using wav2letter++.<br>
[Qibin Chen](https://www.qibin.ink), Zhaoqing Xu, Kai Chen

## Prerequisites

- Linux
- Singularity >= 2.5.1
- Python 3

## Getting Started

### Installation

Clone this repo.

```bash
git clone https://github.com/qibinc/GSoC-2019-ASR-Pipeline
cd GSoC-2019-ASR-Pipeline
```

Please download the Singularity container (with built wav2letter++) by

```bash
singularity pull shub://qibinc/singularity_containers:wav2letter
```

### Next Steps

#### Training

For training with 1 GPU, run `make train`. For distributed training on 8 GPUs, run `make distrib_train`. Have a look at `Makefile` and change the training configuration files to try various hyper-parameters / architectures.

#### Testing

Run `make test` and you can see the predicted texts and their ground truths. The final score will be printed at the final line, e.g., `[total WER: 60.8974%, total LER: 9.02436%, time: 364.033s]`.

## TODOLIST

- [x] Set up the Singularity container for running experiments
- [x] Split Chinese audios using VAD (Voice Activity Detection) Tools
- [x] ASR for English using wav2letter++ (for sanity check)
- [x] ASR for Chinese using wav2letter++ (demo)
- [ ] (Ongoing) Deploying ASR for Chinese as a pipeline

## Acknowledgement

- This work is based on the [wav2letter](https://github.com/facebookresearch/wav2letter) toolkit released by FAIR (Facebook AI Research).
