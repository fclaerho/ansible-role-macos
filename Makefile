# Copyright © 2016 fclaerhout.fr — released under the MIT license.

BUILD_PATH := .build

.PHONY: all check clean

all: check files/macos clean

check:
	$(MAKE) -f dummyplaybook.make check BUILD_PATH=$(BUILD_PATH)

.build/macos: macos.py $(wildcard library/*.py)
	$(MAKE) -f pyz.make\
		BUILD_PATH=$(BUILD_PATH)\
		MAIN_FILE=macos.py\
		SRC_FILES="$(wildcard library/*.py)"\
		TGT_NAME=macos

files/macos: .build/macos
	@cp $< $@

clean:
	@-rm -rf $(BUILD_PATH)
