# Copyright © 2016 fclaerhout.fr — released under the MIT license.
# Type "make" for help.
# See http://stackoverflow.com/a/649462 for multiline variables in makefiles.

PATH := .test

define _PLAYBOOK_YML
---
- hosts: localhost
  roles:
  - ansible-role-macos
endef

export _PLAYBOOK_YML

define _ANSIBLE_YML
[defaults]
retry_files_enabled: False
roles_path: ../..
endef

export _ANSIBLE_YML

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

$(PATH)/ansible.cfg: | $(PATH)
	@echo "$$_ANSIBLE_YML" > $@

$(PATH):
	@mkdir $@

check: $(PATH)/playbook.yml $(PATH)/ansible.cfg
	@cd $(PATH) && ansible-playbook playbook.yml
	$(MAKE) clean

clean:
	@-rm -rf $(PATH)
