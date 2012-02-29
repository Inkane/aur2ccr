#!/usr/bin/env python2
# inspired by a bash script from Arch 
# drop in replacement for getmirrors.sh
from __future__ import print_function

import os
import sys
import urllib2
import contextlib
import re

class SmartDict(dict):
    """return 'Any' as fallback if country is not in list"""

    def __missing__(self, key):
        return 'Any'

# get enviroment variables
try:
    apconf = os.environ["apconf"]
except KeyError:
    apconf = "./archrepos.pacman.conf"

try:
    quiet = (os.environ["quiet"] == "1")
except KeyError:
    quiet = False

# all countries accepted by the arch website
valid_countries = [
 'Australia', 'Belarus',  'Belgium',  'Brazil',
 'Bulgaria',  'Canada',  'Chile',  'China',
 'Colombia',  'Czech',  'Denmark',  'Estonia',
 'Finland',  'France',  'Germany',  'Great Britain',
 'Greece',  'Hungary',  'India',  'Indonesia',  'Ireland',
 'Israel',  'Italy',  'Japan',  'Kazakhstan',  'Korea',
 'Latvia',  'Luxembourg',  'Macedonia', 'Netherlands',
 'New Caledonia',  'Norway', 'Poland', 'Portugal', 'Romania',
 'Russia', 'Singapore', 'Slovakia', 'South', 'Spain',
 'Sweden', 'Switzerland', 'Taiwan', 'Turkey', 'Ukraine',
 'United States', 'Uzbekistan', 'Any'
 ]
alt_country_names = SmartDict() # store alternate country names
alt_country_names["United Kingdom"] = "Great Britain"

# the webadresses of duckduckgo and arch linux 
duckduckgo = "https://duckduckgo.com/lite/?q=ip"
# American proxy
#duckduckgo2 = "http://www.americanproxy.org/browse.php?u=http%3A%2F%2Fduckduckgo.com%2Flite%2F%3Fq%3Dip&b=0" 
archlinux = "http://www.archlinux.org/mirrorlist/?country={}&protocol=ftp&protocol=http&ip_version=4&use_mirror_status=on"

def download(url):
    # downloads a file and returns a file like object if successful
    try:
        webfile = urllib2.urlopen(url)
    except (urllib2.URLError, urllib2.HTTPError):
        print("Opening {} failed because of {}.".format(url,sys.exc_info()), 
                sys.stderr)
        sys.exit(2)
    return contextlib.closing(webfile)

def get_location():
    regex_country = re.compile(r"""
            ,\s # a comma followed by whitespace
              ((?P<oneword>([a-zA-Z])+?)\.) # one-word countries
            | (?P<twoword>(([a-zA-Z])+?\s[a-zA-Z]+))((\s([,(]))) #two-word countries
            """, re.VERBOSE)
    with download(duckduckgo) as coun_file:
        country = ""
        for line in coun_file:
            if "(your IP address)" in line:
                result =  re.search(regex_country, line).groupdict()
                country = result["oneword"] if result["oneword"] else result["twoword"]
                break
    if country not in valid_countries:
        country = alt_country_names[country]
    return country

def main():
    country = get_location()
    if quiet:
        print(country)
        sys.exit(0)
    #create the fitting url
    url = archlinux.format(country)
    with download(url) as mirrorfile:
        for line in mirrorfile:
            if "is not one of the available choiches" in line:
                # should never happen
                print("Something went wrong in getmirrors.py. Please report this  error.", sys.stderr)
                sys.exit(1)
            tmp = re.match("\#(Server.*)",line)
            if tmp:
                # replace $arch with x86_64
                mirror = re.sub("\$arch","x86_64",tmp.group(1))
                break 
    if mirror:
        print(mirror)
    else:
        sys.exit(1)

if __name__ == "__main__":
    main()
