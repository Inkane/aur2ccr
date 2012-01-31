# Makefile for aur2ccr

all: aur2ccr.8.gz

aur2ccr.8.gz : aur2ccr.8
	gzip -c aur2ccr.8 > aur2ccr.8.gz


install: 
#	install -d -m755 
	install -D -m644 aur2ccr.8.gz /usr/local/man/man8/aur2ccr.8.gz