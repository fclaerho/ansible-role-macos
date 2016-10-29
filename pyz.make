# Copyright © 2016 fclaerhout.fr — released under the MIT license.
# Build a standalone executable python archive from modules (PEP 441.)

define _USAGE

Usage:
  make -f pyz.make MAIN_FILE=… SRC_FILES="…" TGT_NAME=…

Variables:
	BUILD_DIR -- build directory [default: .build]
  MAIN_FILE -- entry module path
  SRC_FILES -- space separated list of file paths
  TGT_NAME  -- name of the final executable

Predefined Constants:
  Automatically interpolate __BUILDHASH__ and __TGTNAME__ in MAIN_FILE.
endef

### PUBLIC CONFIGURATION ######################################################

ifndef MAIN_FILE
$(error MAIN_FILE is undefined$(_USAGE))
endif

ifndef SRC_FILES
$(error SRC_FILES is undefined$(_USAGE))
endif

ifndef TGT_NAME
$(error TGT_NAME is undefined$(_USAGE))
endif

BUILD_DIR ?= .build

### PRIVATE IMPLEMENTATION ####################################################

_TGT_FILE := $(BUILD_DIR)/$(notdir $(TGT_NAME))
PYTHON ?= /usr/bin/python
SHELL := /bin/bash -o pipefail

$(_TGT_FILE): $(_TGT_FILE).unittest $(BUILD_DIR)/__main__.py $(SRC_FILES) | $(BUILD_DIR)
	zip --junk-paths $@.zip $(filter %.py, $^)
	echo '#!$(PYTHON)' > $@
	cat $@.zip >> $@
	chmod +x $@
	$@ --version | xargs -I{} echo "Version {}"

$(_TGT_FILE).unittest: $(SRC_FILES) | $(BUILD_DIR)
ifdef TESTS_DIRS
	$(PYTHON) -m unittest discover -v $(TESTS_DIRS)
endif
	touch $@

$(BUILD_DIR)/__main__.py: $(MAIN_FILE) $(SRC_FILES) | $(BUILD_DIR)
	cat $^ | md5 | xargs -I{} sed -e 's@__BUILDHASH__@{}@g' -e 's@__TGTNAME__@$(TGT_NAME)@g' $< > $@

$(BUILD_DIR):
	mkdir -p $(BUILD_DIR)
