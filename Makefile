# Copyright © 2016 fclaerhout.fr — released under the MIT license.

BUILD_DIR := .build

.PHONY: all check clean install

all: check files/macos clean

install:
	$(MAKE) -f dummyplaybook.make install

check:
	$(MAKE) -f dummyplaybook.make check BUILD_DIR=$(BUILD_DIR)

.build/macos: macos.py $(wildcard library/*.py)
	$(MAKE) -f pyz.make\
		BUILD_DIR=$(BUILD_DIR)\
		MAIN_FILE=macos.py\
		SRC_FILES="$(wildcard library/*.py)"\
		TGT_NAME=macos

files/macos: .build/macos
	@cp $< $@

clean:
	@-rm -rf $(BUILD_DIR)
