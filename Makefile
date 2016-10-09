# Copyright © 2016 fclaerhout.fr — released under the MIT license.

BUILD_PATH := .check

define _USAGE
Generates and run a dummy playbook to test this dir as a role.

Usage:
  make RULE...

Rules:
  usage   -- output this help message and exit
  install -- 1st install Ansible on macOS
  check   -- generate and run test in $(BUILD_PATH)
  clean   -- delete $(BUILD_PATH)
endef

export _USAGE

define _PLAYBOOK_YML
---
- hosts: localhost
  gather_facts: False
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

# <tracker 201610081413>
# localhost:
# - is predefined in v2+
# - needs to be defined explicitly, if the inventory file is empty, in v1.x
_ANSIBLE_MAJOR := $(shell ansible --version | grep ansible | cut -b9)
ifeq ($(_ANSIBLE_MAJOR),1)
define _INVENTORY_CFG
localhost ansible_connection=local
endef
export _INVENTORY_CFG
$(BUILD_PATH)/inventory.cfg: | $(BUILD_PATH)
	@echo "$$_INVENTORY_CFG" > $@
check: $(BUILD_PATH)/inventory.cfg
endif
# </tracker>

export PATH := $(PATH):~/Library/Python/2.7/bin:~/.local/bin

.PHONY: usage install check clean

usage:
	@echo "$$_USAGE"

install:
	@easy_install --user ansible

$(BUILD_PATH)/playbook.yml: | $(BUILD_PATH)
	@echo "$$_PLAYBOOK_YML" > $@

$(BUILD_PATH)/ansible.cfg: | $(BUILD_PATH)
	@echo "$$_ANSIBLE_CFG" > $@

$(BUILD_PATH):
	@mkdir $@

check: $(BUILD_PATH)/playbook.yml $(BUILD_PATH)/ansible.cfg
	@cd $(BUILD_PATH) && ansible-playbook playbook.yml
	@$(MAKE) clean

clean:
	@-rm -rf $(BUILD_PATH)
