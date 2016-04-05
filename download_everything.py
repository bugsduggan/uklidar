#!/usr/bin/env python2.7

# You might need to change/remove the shebang line at the top to run this in
# windows, just make sure you're running it in python2.7 and it should work.
#
# You will need to download a library called requests. I'm really not sure how
# that magic works on windows. If you get really stuck, give me a shout and I'll
# google it for you ;)
#
# This should dump a bunch of zip files into a raw_data directory and then
# extract them all. Hopefully some of the code makes sense?
#
# Trying this out with the first couple of files (I don't have enough
# disk/patience to actually run this beast) it seems that each zip file takes
# just under a minute (on average) to download and unzip. I have made no attempt
# to paralellize this (although it's doable); I'm expecting you to be able to
# run this on your big metal at the uni.
#
#
# This code has taken 1.5 beers to produce

from pydata import *

catalog = get_json_catalog()
print 'Oh boy, going to download %d zip files' % len(catalog)
for chunk in catalog:
    print 'Fetching %s' % chunk['url'].split('/')[-1]
    zip_file = download_zip_file(chunk['url'])
    print 'Unzipping %s' % zip_file
    unzip_file(zip_file)
