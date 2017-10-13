# getpaper.py - a janky, hacky script for downloading scientific papers

getpaper.py is an ugly but functional tool for downloading scientific papers
from open access providers in pdf and xml format. It was very much written
to scratch a personal itch for my research purposes but feel free to use it.


## What this doesn

You can pass in one or many URLS of scientific papers to this script. It will
try to download each of those articles. It will prefer XML formats (Pubmed DTD)
over PDF formats but it will download whichever one it can get hold of.

## Which sites it works for

This script currently handles URLS pointing to articles at the following
places. Asterix (*) denotes a wildcard meaning any URL that matches the given
string should work.

 - http://arxiv.org/abs/*
 - http://arxiv.org/pdf/*
 - http://www.plosone.org/article/*
 - http://www.plosbiology.org/article/*
 - http://www.ncbi.nlm.nih.gov/pubmed/*
 - http://rsta.royalsocietypublishing.org/content/*
 - http://rspb.royalsocietypublishing.org/lookup/doi/*
 - http://journals.plos.org/*
 - http://www.plosone.org/article/*
 - http://www.plosbiology.org/article/*
 - http://www.plospathogens.org/article/*,
 - http://www.plosmedicine.org/article/*



## How to install it

Assuming you have a python3 installation just run `python setup.py install`.

## How to use as a CLI

Simply run `./getpaper <url> [<url2> <url3> ...]`

## How to use as a library

import getpaper and call `getpaper.get_science_paper(url)`.
