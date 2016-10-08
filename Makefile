# Copyright © 2016 fclaerhout.fr — released under the MIT license.
# Type "make" for help.
# See http://stackoverflow.com/a/649462 for multiline variables in makefiles.

PATH := .check

define _PLAYBOOK_YML
---
- hosts: localhost
  roles:
  - ansible-role-macos
endef

# Required for Ansible < 2
define _INVENTORY_CFG
localhost
endef

define _ANSIBLE_CFG
[defaults]
retry_files_enabled: False
roles_path: ../..
inventory: inventory.cfg
#hostfile: inventory.cfg # Ansible < 1.9
endef

export _PLAYBOOK_YML
export _INVENTORY_CFG
export _ANSIBLE_CFG

.PHONY: usage check clean

usage:
	@echo "Usage:"
	@echo "  make RULE..."
	@echo
	@echo "Rules:"
	@echo "  usage -- output this help message and exit"
	@echo "  check -- generates and play a dummy playbook to test this role"
	@echo "  clean -- delete test byproducts"

$(PATH)/playbook.yml: | $(PATH)
	@echo "$$_PLAYBOOK_YML" > $@

$(PATH)/inventory.cfg: | $(PATH)
	@echo "$$_INVENTORY_CFG" > $@

$(PATH)/ansible.cfg: | $(PATH)
	@echo "$$_ANSIBLE_YML" > $@

$(PATH):
	@mkdir $@

check: $(PATH)/playbook.yml $(PATH)/inventory.cfg $(PATH)/ansible.cfg
	@cd $(PATH) && ansible-playbook playbook.yml
	$(MAKE) clean

clean:
	@-rm -rf $(PATH)
