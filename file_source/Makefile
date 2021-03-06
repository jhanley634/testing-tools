
FILE_SOURCE = /tmp/file_source
FS = $(FILE_SOURCE)

PKGS = `cat $(FS)/pkgs.txt`

all:  $(FS)/full.tar.gz $(FS)/du-xk.txt

$(FS)/dpkg-l.txt:
	mkdir -p $(FS)/pkg
	dpkg -l | egrep '^ii ' > $(FS)/dpkg-l.txt
	src/install_modules.jl

# Suffixes like ':amd64' will not appear in pkgs.txt.
$(FS)/pkgs.txt: $(FS)/dpkg-l.txt
	test -r $@ || touch $@
	mv $@ $@~
	tr ':' ' ' < $< | awk '{print $$2}' | sort > $@
	diff -u $@~ $@ || true

$(FS)/du-xk.txt:
	du -xk / > $@ || true
	test -r $@~ || cp -p $@ $@~

EXCLUDE='\.pyc ?$$|\.elc ?$$| /boot/swap[1500M]* ?$$| /boot/initrd.img-.*-generic ?$$| /boot/grub/i386-pc/.*\.mod ?$$| /var/log/installer/cdebconf/templates.dat ?$$| /var/lib/texmf/web2c/luatex/.*.fmt ?$$| /boot/grub/.*unicode.pf2 ?$$| /usr/lib/locale/locale-archive ?$$| /lib/modules/.*\.(alias|bin) ?$$| /lib/udev/hwdb.bin ?$$| /var/log/btmp ?$$| /tmp/file_source/.*|/.julia/.cache/.*| /var/lib/dpkg/info/.*| /var/lib/apt/lists/.*| /var/cache/.*'

$(FS)/find.txt: $(FS)/pkgs.txt
	find / -xdev -printf "%CY-%Cm-%Cd %CH:%CM %T@ %M %7u %3n %7i  %p %l\n" | egrep -v $(EXCLUDE) > $@
	test -r $@~ || cp -p $@ $@~
	for PKG in $(PKGS); do ./pkg_to_db.sh $(FS) $$PKG; done

$(FS)/git_repos.txt: $(FS)/find.txt
	cat $< | awk '/\/.git ?$$/ {print $$8}' | sed 's;/.git$$;;' > $@
	@./store_working_file_names.py $(FS) '[clean]'
	for REPO in `cat $@`; do ./store_working_file_names.py $(FS) $$REPO; done

$(FS)/files_to_backup.txt: $(FS)/git_repos.txt
	src/backup_report.jl | sed 's/^.//' | sort > $@
	test -r $@~ || cp -p $@ $@~

$(FS)/full.tar.gz: $(FS)/files_to_backup.txt
	GZIP='--rsyncable' tar zcf $@ -C / --files-from $<
	tar ztf $@ | diff -wu $< -
	test -r $@~ || cp -p $@ $@~
	ls -l $@*

clean:
	rm -rf $(FS)
