# Makefile for aur2ccr
manpages = aur2ccr.8.gz
binfiles = aur2ccr getmirrors.sh
unstable = aur2ccr-unstable
configs = names.conf aur2ccr.conf archrepos.pacman.conf
others = aur2ccr.8 Makefile README
allfiles = $(binfiles) $(configs) $(manpages) $(others)

all: man $(allfiles)
	sh -c "country= arch=$(echo $MACHTYPE|grep -o '^\w*') getmirrors.sh"

man: aur2ccr.8.gz $(others)

install: $(allfiles) install-man
	install -d -m755 "$(DESTDIR)/usr/bin"
	install -d -m755 "$(DESTDIR)/etc/aur2ccr"
	install -D -m755 $(binfiles) "$(DESTDIR)/usr/bin/"
	install -D -m644 $(configs) "$(DESTDIR)/etc/aur2ccr/"

install-unstable: $(allfiles) install-man # this will install the aur2ccr-unstable script, use with caution
	install -d -m755 "$(DESTDIR)/usr/bin"
	install -d -m755 "$(DESTDIR)/etc/aur2ccr"
	install -D -m755 $(unstable) "$(DESTDIR)/usr/bin/"
	install -D -m644 $(configs) "$(DESTDIR)/etc/aur2ccr/"

install-man: # 'make install' calls this, so only do 'make install-man' if all you want is the man page.
	install -d -m755 "$(DESTDIR)/usr/man/man8"
	install -D -m644 $(manpages) "$(DESTDIR)/usr/man/man8/"

aur2ccr.8.gz : $(others)
	gzip -c aur2ccr.8 > aur2ccr.8.gz

bundle: aur2ccr.txz.sh $(allfiles) # This is for the distributer ONLY, you need my 'bundle>=0.9' to use it.

aur2ccr.txz.sh : $(allfiles)
	bundle -s -x * > aur2ccr.txz.sh

