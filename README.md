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

Please download the Singularity container (with dependencies) by

```bash
singularity pull docker://wav2letter/wav2letter:cuda-latest
```

### Next Steps

...

## TODOLIST

- [x] Set up the Singularity container for running experiments
- [x] Split Chinese audios using VAD (Voice Activity Detection) Tools
- [x] ASR for English using wav2letter++ (for sanity check)
- [ ] ASR for Chinese using wav2letter++ (demo)
- [ ] Deploying ASR for Chinese as a pipeline

## Acknowledgement

- This work is based on the [wav2letter](https://github.com/facebookresearch/wav2letter) toolkit released by FAIR (Facebook AI Research).
