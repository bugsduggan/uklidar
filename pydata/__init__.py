from json import loads
from os import listdir, mkdir
from os.path import isfile, join, isdir
import sys
import zipfile

import requests


MAX_RETRIES = 10


def get_json_catalog(catalog_dir='catalog'):
    """
    This function looks in every json file in the catalog directory and splodges
    all that sexy json data together into one big list.
    """
    onlyfiles = [f for f in listdir(catalog_dir) if isfile(join(catalog_dir, f))]
    onlyfiles = [f for f in onlyfiles if f.endswith('.json')]

    data_points = list()
    for filename in onlyfiles:
        with open(join(catalog_dir, filename), mode='ro') as f:
            data_points.extend(loads(''.join(f.read())))
    return data_points


def download_zip_file(url, directory='raw_data'):
    """
    This will download the zip file to the directory you specify... probably
    """
    if not isdir(directory):
        mkdir(directory)

    local_filename = '%s.zip' % url.split('/')[-1]
    local_filename = join(directory, local_filename)
    # setup a session to handle retries
    session = requests.Session()
    session.mount('http://',
                  requests.adapters.HTTPAdapter(max_retries=MAX_RETRIES))
    session.mount('https://',
                  requests.adapters.HTTPAdapter(max_retries=MAX_RETRIES))

    r = session.get(url, stream=True)
    # handle basic HTTP errors
    try:
        r.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print >> sys.stderr, e.message()
        raise e

    with open(local_filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024): 
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)

    return local_filename


def unzip_file(filename):
    """
    This will unzip a file into its own directory.
    """
    directory = filename.split('.')[0]
    if not isdir(directory):
        mkdir(directory)
    with zipfile.ZipFile(filename, 'r') as f:
        if f.testzip():
            raise Exception('bad zip file')
        f.extractall(directory)
