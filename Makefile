# Makefile for aur2ccr and aur2ccr-unstable
manpages = aur2ccr.8.gz
binfiles = aur2ccr getmirrors.py
unstable = aur2ccr-unstable
configs = names.conf aur2ccr.conf archrepos.pacman.conf
others = aur2ccr.8 Makefile
allfiles = $(binfiles) $(configs) $(manpages) $(others) README.md

all: man $(others)
	python2 getmirrors.py --quiet
	@echo "run 'aur2ccr -s' if the above server is incorrect"

man: aur2ccr.8.gz $(others)

install: $(allfiles) install-man
	install -d -m755 "$(DESTDIR)/usr/bin"
	install -d -m755 "$(DESTDIR)/etc/aur2ccr"
	install -D -m755 $(binfiles) "$(DESTDIR)/usr/bin/"
	install -D -m644 $(configs) "$(DESTDIR)/etc/aur2ccr/"

uninstall: # not ready for use
	rm -rf "$(DESTDIR)/etc/aur2ccr"

install-unstable: $(allfiles) # this will install the aur2ccr-unstable script, use with caution - assumes 'make install' already done.
	install -d -m755 "$(DESTDIR)/usr/bin"
	install -D -m755 $(unstable) "$(DESTDIR)/usr/bin/"

install-man: # 'make install' calls this, so only do 'make install-man' if all you want is the man page.
	install -d -m755 "$(DESTDIR)/usr/share/man/man8"
	install -D -m644 $(manpages) "$(DESTDIR)/usr/share/man/man8/"

aur2ccr.8.gz : $(others)
	gzip -c aur2ccr.8 > aur2ccr.8.gz

bundle: aur2ccr.txz.sh $(allfiles) # This is for the distributer only, you need my 'bundle>=0.9' to use it.

aur2ccr.txz.sh : $(allfiles)
	bundle -s -x * > aur2ccr.txz.sh
