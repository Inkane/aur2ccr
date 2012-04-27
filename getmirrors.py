#!/usr/bin/env python2
# inspired by a bash script from Arch
# drop in replacement for getmirrors.sh
from __future__ import print_function

import os
import sys
import urllib2
import contextlib
import re
import fileinput
import logging

logging.basicConfig(level=logging.DEBUG, format='>>%(levelname)s:  %(message)s')


# needed for a trick to get a mirror if the user lives in an unknown country
class SmartDict(dict):
    """return 'Any' as fallback if country is not in list"""

    def __missing__(self, key):
        return 'all'

# get enviroment variables
try:
    paconf = os.environ["paconf"]
except KeyError:
    paconf = "./archrepos.pacman.conf"

# quiet mode
if "--quiet" in sys.argv:
    quiet = True
else:
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
 'Russia', 'Singapore', 'Slovakia', 'South Korea', 'Spain',
 'Sweden', 'Switzerland', 'Taiwan', 'Turkey', 'Ukraine',
 'United States', 'Uzbekistan', 'all'
 ]
alt_country_names = SmartDict()  # store alternate country names
alt_country_names["United Kingdom"] = "GB"
alt_country_names["Argentina"] = "Brazil"
alt_country_names["USA"] = "US"
alt_country_names["Australia"] = "AU"
alt_country_names["Belarus"] = "BY"
alt_country_names["Belgium"] = "BE"
alt_country_names["Brazil"] = "BR"
alt_country_names["Bulgaria"] = "BG"
alt_country_names["Canada"] = "CA"
alt_country_names["Chile"] = "CL"
alt_country_names["China"] = "CN"
alt_country_names["Colombia"] = "CO"
alt_country_names["Czech Republic"] = "CZ"
alt_country_names["Denmark"] = "DK"
alt_country_names["Estonia"] = "EE"
alt_country_names["Finland"] = "FI"
alt_country_names["France"] = "FR"
alt_country_names["Germany"] = "DE"
alt_country_names["Greece"] = "GR"
alt_country_names["Hungary"] = "HU"
alt_country_names["India"] = "IN"
alt_country_names["Indonesia"] = "ID"
alt_country_names["Ireland"] = "IE"
alt_country_names["Israel"] = "IL"
alt_country_names["Italy"] = "IT"
alt_country_names["Japan"] = "JP"
alt_country_names["Kazakhstan"] = "KZ"
alt_country_names["Korea"] = "KR"
alt_country_names["Latvia"] = "LV"
alt_country_names["Luxembourg"] = "LU"
alt_country_names["Macedonia"] = "MG"
alt_country_names["Netherlands"] = "NL"
alt_country_names["New Caledonia"] = "NC"
alt_country_names["Norway"] = "NO"
alt_country_names["Poland"] = "PL"
alt_country_names["Portugal"] = "PT"
alt_country_names["Romania"] = "RO"
alt_country_names["Russian Federation"] = "RU"
alt_country_names["Russian"] = "RU"
alt_country_names["Serbia"] = "RS"  # RS?
alt_country_names["Singapore"] = "SG"
alt_country_names["Slovakia"] = "SK"
alt_country_names["South Africa"] = "ZA"
alt_country_names["Spain"] = "ES"
alt_country_names["Sri Lanka"] = "LK"
alt_country_names["Sweden"] = "SE"
alt_country_names["Switzerland"] = "CH"
alt_country_names["Taiwan"] = "TW"
alt_country_names["Turkey"] = "TR"
alt_country_names["Ukraine"] = "UA"
alt_country_names["United States"] = "US"
alt_country_names["Uzbekistan"] = "UZ"
alt_country_names["Viet Nam"] = "VN"
alt_country_names["Vietnam"] = "VN"

# the webadresses of duckduckgo and arch linux
duckduckgo = "https://duckduckgo.com/lite/?q=ip"
archlinux = "http://www.archlinux.org/mirrorlist/?country={}&protocol=ftp&protocol=http&ip_version=4&use_mirror_status=on"


def download(url):
    # downloads a file and returns a file like object if successful
    try:
        webfile = urllib2.urlopen(url)
    except (urllib2.URLError, urllib2.HTTPError):
        print("Opening {} failed because of {}.".format(url, sys.exc_info()),
                sys.stderr)
        sys.exit(2)
    return contextlib.closing(webfile)


def get_location():
    logging.info("Determining your location...")
    regex_country = re.compile(r"""
            ,\s # a comma followed by whitespace
              ((?P<oneword>([a-zA-Z])+?)\.) # one-word countries
            | (?P<twoword>(([a-zA-Z])+?\s[a-zA-Z]+))((\s([,(]))|\.) #two-word countries
            """, re.VERBOSE)
    with download(duckduckgo) as coun_file:
        country = ""
        for line in coun_file:
            logging.debug(line)
            if "(your IP address)" in line:
                try:
                    result = re.search(regex_country, line).groupdict()
                    logging.debug("The result is {}".format(result))
                except AttributeError:
                    # if the regex doesn't match it returns None
                    # None has no groupdict attribute, thus resulting in
                    # AttributeError
                    # this should never fail until the duckduckgo website changes
                    logging.error(line)
                    logging.warn("Oh no! DuckDuckGo doesn't know where you live!\nWe'll use a generic server for now. For better performance you should run aur2ccr --setup\n")
                    return "all"
                country = result["oneword"] if result["oneword"] else result["twoword"]
                break
    # test if there is a mirror list for the country
    if country not in valid_countries:
        country = alt_country_names[country]
    return country


def edit_conf(server, file=paconf):
    regex = re.compile("Server = .*\$")
    for line in fileinput.input(file, inplace=1):
        if re.match(regex, line):
            #  if the line contains Server, replace it with the new server
            print(server)
        else:  # else don't change anything
            print(line, end="")


def main():
    country = get_location()

    # Give the user the chance to change the mirror if not in quiet mode
    if not quiet:
        usercountry = raw_input("Please enter your country: (leave blank to use {}): ".format(country))
        if usercountry:
            country = alt_country_names[usercountry]
    logging.debug("country={}".format(country))

    #create the fitting url
    url = archlinux.format(urllib2.quote(country))
    mirror = ""
    print("Generating pacman configuration for {}".format(paconf))
    with download(url) as mirrorfile:
        logging.info("Determining the best mirror...")
        for line in mirrorfile:
            if "is not one of the available choiches" in line:
                # should never happen
                logging.error("Something went wrong in getmirrors.py. Please report this error.")
                sys.exit(1)
            tmp = re.match("\#(Server.*)", line)
            if tmp:
                # replace $arch with x86_64
                mirror = re.sub("\$arch", "x86_64", tmp.group(1))
                break
    if mirror:
        print(mirror)
    else:
        sys.exit(1)
    logging.info("Editing the config file...")
    edit_conf(mirror)

if __name__ == "__main__":
    main()
