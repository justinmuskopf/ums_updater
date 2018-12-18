import requests
from bs4 import BeautifulSoup
from sys import argv
from os import environ
import subprocess

# This is where we get the most recent version from
V_URL     = 'https://www.universalmediaserver.com/'
NIX_DL_ID = 'DownloadLinux'

# This is where we download the tarball from
SF_DL_URL = 'http://sourceforge.net/projects/unimediaserver/files/Official%20Releases/Linux/{}/download'

# wget command predecessor
WGET_CMD  = ['wget', '-O']

TAR_CMD = ['tar', '-xvzf']

VERSION_FILE = str(environ.get('UMS_HOME')) + '/CHANGELOG.txt'
try:
    with open(VERSION_FILE) as f:
        current_version = f.readline().split(' ')[0]
except IOError:
    print("Could not open {}... Defaulting to overwrite.".format(VERSION_FILE))

# oops
def die(die_string = '', code = 0):
    if die_string:
        print(die_string)
    else:
        print('{}: An unknown error occurred!'.format(argv[0]))

    exit(code)

def version_is_newer(new, current):
    new_arr = [int(x) for x in new.split('.')]
    cur_arr = [int(x) for x in current.split('.')]

    for idx, val in enumerate(new_arr):
        if idx >= len(cur_arr):
            return True

        if val > cur_arr[idx]:
            return True
        elif val < cur_arr[idx]:
            return False

    return False

# Get content from version site
request = requests.get(V_URL)
if request.status_code != 200:
    die('Could not contact {}!'.format(V_URL))

# Get BS object from html
soup = BeautifulSoup(request.content, features = 'html.parser')

# Loop through all 'a' tags
for a_tag in soup.findAll('a'):
    # IS THIS WHO WE ARE LOOKING FOR
    if a_tag.get('id') == NIX_DL_ID:
        # Get the URL and name from this boi
        dl_url = a_tag.get('href')
        filename = dl_url.split('=')[-1]
        new_version = filename.replace(".tgz", "")[4:]

        # Add to that there command
        WGET_CMD.append(filename)
        WGET_CMD.append(SF_DL_URL.format(filename))

        break


# Same or newer already installed
if not version_is_newer(new_version, current_version):
    die('Same or newer version already installed! (v{} vs v{})'.format(new_version, current_version))

# Call that there command (blocking)
subprocess.call(WGET_CMD)

