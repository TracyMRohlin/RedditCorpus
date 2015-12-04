#!/usr/bin/env python

from split_training_testing import *



if __name__ == "__main__":
    wd = raw_input("Please enter the filepath where the the corpus files are saved\n")
    onlyfiles = [f for f in os.listdir(wd) if isfile(join(wd,f)) and "Untagged" not in f][1:]
    create_nontesting(onlyfiles, wd, 0.6, "training")
    create_nontesting(onlyfiles, wd, 0.5, "validation")
    create_testing(onlyfiles, wd)