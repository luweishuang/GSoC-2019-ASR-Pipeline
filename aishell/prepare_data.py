"""
Command : prepare_data.py --src [...] --dst [...]
"""
import argparse
import os
import sys

from tqdm import tqdm

def findaudiofiles(dir):
    files = []
    for dirpath, _, filenames in os.walk(dir):
        for filename in filenames:
            if filename.endswith(".wav"):
                files.append(os.path.join(dirpath, filename))
    return files


def write_sample(filename, idx, dst, transcripts_dict):

    # filename, input, lbl = line.split(" ", 2)

    # assert filename and input and lbl

    basepath = os.path.join(dst, "%09d" % idx)
    name = os.path.splitext(os.path.basename(filename))[0]
    if name not in transcripts_dict:
        return False

    # wav
    os.system(
        "cp {src} {dst}".format(
            src=filename,
            dst=basepath + ".wav",
        )
    )

    # wrd
    words = transcripts_dict[name].strip()
    with open(basepath + ".wrd", "w", encoding="utf-8") as f:
        f.write(words)

    # ltr
    spellings = " | ".join([" ".join(w) for w in words.split()])
    with open(basepath + ".tkn", "w", encoding="utf-8") as f:
        f.write(spellings)

    # id
    with open(basepath + ".id", "w") as f:
        f.write("file_id\t{fid}".format(fid=idx))

    return True

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Aishell Dataset creation.")
    parser.add_argument("--src", help="source directory")
    parser.add_argument("--dst", help="destination directory", default="./aishell")

    args = parser.parse_args()

    assert os.path.isdir(
        str(args.src)
    ), "Aishell src directory not found - '{d}'".format(d=args.src)

    transcript_subpath = os.path.join(args.src, "transcript/aishell_transcript_v0.8.txt")
    transcripts_dict = {}
    with open(transcript_subpath, 'r', encoding="utf-8") as f:
        for line in f:
            fname, transcript = line.split(None, 1)
            transcripts_dict[fname] = transcript

    subpaths = ["wav/train", "wav/dev", "wav/test"]

    os.makedirs(args.dst, exist_ok=True)

    for subpath in subpaths:
        src = os.path.join(args.src, subpath)
        dst = os.path.join(args.dst, "data", subpath)
        os.makedirs(dst, exist_ok=True)

        wavs = []
        assert os.path.exists(src), "Unable to find the directory - '{src}'".format(
            src=src
        )

        sys.stdout.write("analyzing {src}...\n".format(src=src))
        sys.stdout.flush()
        wavfiles = findaudiofiles(src)
        # transcriptfiles.sort()
        sys.stdout.write("writing to {dst}...\n".format(dst=dst))
        sys.stdout.flush()

        idx = 0
        n_samples = len(wavfiles)
        for n in tqdm(range(n_samples)):
            idx += write_sample(wavfiles[n], idx, dst, transcripts_dict)

    # create tokens dictionary
    tkn_file = os.path.join(args.dst, "data", "wav/tokens.txt")
    sys.stdout.write("creating tokens file {t}...\n".format(t=tkn_file))
    sys.stdout.flush()
    with open(tkn_file, "w") as f:
        f.write("|\n")
        tokens = set()
        for key in transcripts_dict:
            chars = list(transcripts_dict[key].strip().replace(' ', ''))
            for char in chars:
                tokens.add(char) 
        for token in tokens:
            f.write(token + "\n")
        # f.write("'\n")
        # for alphabet in range(ord("a"), ord("z") + 1):
        #     f.write(chr(alphabet) + "\n")

    sys.stdout.write("Done !\n")
