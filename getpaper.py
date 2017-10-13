#!/usr/bin/env python3

import os
import json
import sys
import requests

from collections import Counter
from urllib.parse import urlparse


def get_science_paper(url_str, data_dir="papers", cache="downloaded.json"):
    """Retrieve a scientific paper from a URL or return None if not possible"""

    domains = Counter()

    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

    url = urlparse(url_str)
    cached = {}

    domains[url.netloc] += 1

    if os.path.exists(cache):
        try:
            with open(cache,"r") as f:
                cached = json.load(f)
        except Exception as e:
            print("Could not load pmc cache")

    if "royalsocietypublishing.org" in url.netloc:

        if url.path.startswith("/content/"):

            pdfurl = url_str.split("?")[0] + ".full.pdf"

            pdfname = pdfurl.split("/")[-1]
            savepath = os.path.join(data_dir, pdfname)

        elif url.path.startswith("/lookup/doi/"):

            #need to execute lookup to get the pdf
            r = requests.get(url_str)

            print("Redirected from {} => {}".format(url_str, r.url))

            pdfurl = r.url.split("?")[0] + ".full.pdf"

            pdfname = pdfurl.split("/")[-1]
            savepath = os.path.join(data_dir, pdfname)


        if savepath is not None and pdfurl is not None:
            if os.path.exists(savepath):
                print("Refusing to overwrite existing paper {}".format(pdfname))
            else:
                r = requests.get(pdfurl)

                with open(savepath,"wb") as f:
                    f.write(r.content)

            return savepath
        else:
            print("No PDF found")


    if url.netloc == "arxiv.org":

        savename = None
        pdfurl = None


        if url.path.startswith("/pdf/"):

            savename = os.path.join(data_dir,os.path.basename(url.path))
            pdfurl = url_str

        if url.path.startswith("/abs/"):
            pdfurl = url_str.replace("/abs/","/pdf/") + ".pdf"
            print(pdfurl)
            filename = pdfurl.split("/")[-1]
            savename = os.path.join(data_dir,filename)


        if savename is not None and pdfurl is not None:
            if not os.path.exists(savename):
                print("Saving arxiv paper")
                r = requests.get(pdfurl)
                with open(savename,"wb") as f:
                    f.write(r.content)
            else:
                print("Refusing to overwrite arxiv article {}".format(savename))

            return savename

        else:
            print("Can't find PDF url for {}".format(url_str))




    if url.netloc == "www.ncbi.nlm.nih.gov":

        if url.path.startswith("/pubmed/"):
            pmid = url.path[8:]

            if not re.match("[0-9]+",pmid):
                print("Oops, that's not a pmid")
                return

            if pmid in pmc_downloaded and pmc_downloaded[pmid] is None:
                print("Stored a none for this PMID so it probably doesn't work...")
            elif pmid in pmc_downloaded and os.path.exists(pmc_downloaded[pmid]):
                print("Cowardly refusing to overwrite Pubmed paper...")
            else:
                print("Found PMID: " + pmid)

                pm_paper = get_pmc_paper_from_id(pmid)

                pmc_downloaded[pmid] = pm_paper

                with open(pmc_cache,"w") as f:
                    json.dump(pmc_downloaded,f)



        return pmc_downloaded[pmid]

    if url.netloc == "journals.plos.org":

        # don't try and faff about with comments
        if url.path.startswith("/plosone/article/comment"):
            return

        try:
            qs = parse_qs(url.query)
            pid = qs['id'][0]
        except Exception as e:
            print(qs)
            print("Error parsing {}".format(paper), e)

        filename = os.path.join("../data/guardian_news/papers/",
                                "{}.xml".format(pid.replace("/","_").strip()))

        if os.path.exists(filename):
            print("not overwriting file {}... skipping...".format(filename))

        else:
            print("Downloading {}".format(url))

            paper = requests.get("http://journals.plos.org/plosone/article/file",
                                 params={"id":pid, "type":"manuscript"})

            with open(filename,"w") as f:
                f.write(paper.text)

        return filename

    if url.netloc == "dx.plos.org":

        filename = "../data/guardian_news/papers/{}.xml".format(unquote(url.path[1:]).replace("/","_").strip())

        if os.path.exists(filename):
            print("not overwriting file {}... skipping...".format(filename))

        else:
            print("Downloading {}".format(url))

            paper = requests.get("http://journals.plos.org/plosone/article/file",
                         params={"id":unquote(url.path[1:]), "type":"manuscript"})

            with open(filename,"w") as f:
                f.write(paper.text)

        return filename


    if url.netloc in ["www.plosone.org",
                      "www.plosbiology.org",
                      "www.plospathogens.org",
                      "www.plosmedicine.org"]:


        # split on . => (www, plosone, org)
        journal = url.netloc.split(".")[1]

        if url.path.startswith("/annotation/listThread.action"):
            return

        fileid = unquote(url.path[22:]).strip()

        if url.path.startswith("/article/info:doi/"):
            fileid = url.path[18:].strip()

        elif url.path.startswith("/article/info:doi%2F"):
            fileid = unquote(url.path[20:]).strip()

        elif url.path.startswith("/doi/"):
            fileid = "10.1371/journal."+unquote(url.path[5:]).strip()

        elif url.path.startswith("/article/info%253Adoi%252F"):
            fileid = unquote(url.path[26:]).strip()

        filename = os.path.join(data_dir,
                                "{}.xml"
                                .format(unquote(fileid)
                                        .replace("/", "_")
                                        )
                                )

        if os.path.exists(filename):
            print("not overwriting file {}... skipping...".format(filename))
        else:
            print("Downloading {}".format(url))

            paper = requests.get("http://journals.plos.org/{}/article/file".format(journal),
                                 params={"id":unquote(fileid), "type":"manuscript"})


            with open(filename,"w") as f:
                f.write(paper.text)

        return filename

    # IF the url didn't match above rules, dump to file
    return None

def main():

    if len(sys.argv) < 2:
        print("Please provide some papers to go get")

    for arg in sys.argv[1:]:
        get_science_paper(arg)


if __name__ == "__main__":
    main()
