#!/usr/bin/env python2
import sys
import os
import urllib2
import contextlib
import re

countries = dict()
countries["United Kingdom"] = "Great Britain"
duckduckgo = "https://duckduckgo.com/lite/?q=ip"
archlinux = "http://www.archlinux.org/mirrorlist/?country={}&protocol=ftp&protocol=http&ip_version=4&use_mirror_status=on"

def download(url):
    webfile = urllib2.urlopen(url)
    return webfile

def main():
    # get location of the user
    with contextlib.closing(download(duckduckgo)) as coun_file:
        country = ""
        for line in coun_file:
            if "(your IP address)" in line:
                country =  re.search(",\s(([a-zA-Z])+?)\.", line).group(1)
                break
    if country:
        url = archlinux.format(countries[country] if country in countries else
                    country)
    else:
        url = ""
    with contextlib.closing(download(url)) as mirrorfile:
        for line in mirrorfile:
            tmp = re.match("\#(Server.*)",line)
            if tmp:
                print tmp.group(1)
                #break
            #else:
                #continue
            print line

if __name__ == "__main__":
    main()
