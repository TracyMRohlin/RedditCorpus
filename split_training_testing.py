#!/usr/bin/env python
__author__ = 'tracyrohlin'

import os
import shutil
import random
from pprint import pprint

from os.path import isfile, join, exists


def set_directories(old_wd, method):
    old_wd += "/"
    if method == "training":
        new_wd = old_wd + "training/"
    elif method == "testing":
        new_wd = old_wd + "testing/"
    else:
        new_wd = old_wd + "validation/"

    if not exists(new_wd):
        os.mkdir(new_wd)

    return old_wd, new_wd


def create_nontesting(onlyfiles, old_wd, n, method):
    old_wd, new_wd = set_directories(old_wd, method)
    training_amount = int(len(onlyfiles)*n)
    for _ in range(training_amount):
        file = random.choice(onlyfiles)
        old_file_path = old_wd+file
        new_file_path = new_wd+file
        shutil.move(old_file_path, new_file_path)
        onlyfiles.remove(file)


def create_testing(onlyfiles, old_wd):
    old_wd, new_wd = set_directories(old_wd, "testing")

    for file in onlyfiles:
        old_file_path = old_wd+file
        new_file_path = new_wd+file
        shutil.move(old_file_path, new_file_path)

def split_data():
    onlyfiles = [f for f in os.listdir(".") if str(f).endswith(".txt")]
    wd = "."
    response = raw_input("Would you like to include a validation set?\n")[0].lower()
    if response == "y":
        create_nontesting(onlyfiles, wd, 0.5, "training")
        create_nontesting(onlyfiles, wd, 0.25, "validation")
        create_testing(onlyfiles, wd)

    else:
        create_nontesting(onlyfiles, wd, 0.66, "training")
        create_testing(onlyfiles, wd)


if __name__ == "__main__":
    split_data()