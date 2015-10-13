#!/usr/bin/env python
"""Run tf-idf to identify topic words.

Assumptions:
(1) Ignore title words.
"""

import sys, os, re, math, json
from collections import defaultdict


def count(lines):
    fd = {}
    for line in lines:
        words = line.decode('utf8').strip().split()
        hit = len(words) > 0
        #if hit: hit = re.search('/', words[0])
        if hit:
            for word in words:
                print word
                if not word in fd: fd[word] = 0.0
                fd[word] += 1
    return fd


def dict_idf(path):
    """IDF for all words in path"""
    path += "/"
    fd = {}
    flist = os.listdir(path)
    for file in flist:
        if not str(file).endswith("txt"):
            continue
        ffd = count(open(path + file).readlines())
        for w in ffd:
            if not w in fd: fd[w] = 0.0
            fd[w] += 1
    n = len(flist)
    for w in fd: fd[w] = math.log(n / fd[w])
    return fd


def top(n, post, idf):
    """Top n words in terms of tf-idf."""
    with open(post) as f:
        text = f.readlines()
        del text[0:3]
        tf = count(text)
        out = []
        for w in tf:
            s = tf[w] * idf[w]
            out.append((s, w))
        out.sort();
        out.reverse()
        print out[:n]
        return out[:n]


def karma(lines):
    return lines[1].split()[-1]


if __name__ == '__main__':
    path = sys.argv[1] + "/";
    n = int(sys.argv[2])
    os.chdir(path)
    idf = dict_idf(path)

    with open("New_TFIDF.json", "w") as jsonfile:
        data = defaultdict(str)
        for file in os.listdir("."):
            if not str(file).endswith("txt"):
                continue
            karma_score = karma(open(file).readlines())
            words = []
            for s, w in top(n, path + file, idf):
                #print w
                words.append(w.encode('utf8'))

            data[str(file)] = {'karma':karma_score, 'words':words}
        json.dump(data, jsonfile, indent=4, sort_keys=True)