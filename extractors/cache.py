import os
import codecs

prefix = ""
folder = "cache"


def cache_or_url(fname, url):
    fname = os.path.join(folder, prefix + "_" + fname)
    if os.path.isfile(fname):
        with codecs.open(fname, "r", "utf8") as f:
            data = f.read()
    else:
        r = requests.get(url)
        with codecs.open(fname, "w", "utf8") as f:
            f.write(r.text)
        data = r.text
    return data