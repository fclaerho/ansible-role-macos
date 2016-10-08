# Copyright © 2016 fclaerhout.fr — released under the MIT license.
# Type "make" for help.
# See http://stackoverflow.com/a/649462 for multiline variables in makefiles.

BUILD_PATH := .check

define _PLAYBOOK_YML
---
- hosts: localhost
  roles:
  - ansible-role-macos
endef

define _ANSIBLE_CFG
[defaults]
retry_files_enabled: False
roles_path: ../..
inventory: inventory.cfg
endef

export _PLAYBOOK_YML
export _ANSIBLE_CFG

export PATH := $(PATH):~/Library/Python/2.7/bin:~/.local/bin

.PHONY: usage install check clean

usage:
	@echo "Usage:"
	@echo "  make RULE..."
	@echo
	@echo "Rules:"
	@echo "  usage   -- output this help message and exit"
	@echo "  install -- install Ansible on macOS"
	@echo "  check   -- generates and play a dummy playbook to test this role"
	@echo "  clean   -- delete test byproducts"

install:
	easy_install --user ansible

$(BUILD_PATH)/playbook.yml: | $(BUILD_PATH)
	@echo "$$_PLAYBOOK_YML" > $@

$(BUILD_PATH)/ansible.cfg: | $(BUILD_PATH)
	@echo "$$_ANSIBLE_CFG" > $@

$(BUILD_PATH):
	@mkdir $@

check: $(BUILD_PATH)/playbook.yml $(BUILD_PATH)/ansible.cfg
	@cd $(BUILD_PATH) && ansible-playbook playbook.yml
	$(MAKE) clean

clean:
	@-rm -rf $(BUILD_PATH)
