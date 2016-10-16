
<img alt="Ansible Logo" src="https://github.com/fclaerho/ansible-role-macos/blob/master/ansible-logo.png" align="right" />

_This [Ansible role](https://docs.ansible.com/playbooks_roles.html) brings macOS modules to manage apps, defaults, flags, and packages. It is primarily designed for a local user, to setup a work environment._

[Variables](#variables) | [FAQ](#faq) | [Development](#development)

[![Build Status](https://travis-ci.org/fclaerho/ansible-role-macos.svg?branch=master)](https://travis-ci.org/fclaerho/ansible-role-macos)


Variables
---------

### Apps

Restore (state: present) or purge (state: absent) an app.

Restoring an app does not support a full install and is primarily designed for restoring a configuration.

NOTICE! Purging an app includes its defaults, preferences, support, container and package. Make sure to have a backup of your application defaults beforehand.

| Name | Default | Description |
|------|---------|-------------|
| `macos_apps` | [] | List of dict `{'name', 'state': present/absent, 'domains', 'defaults': path}` |

Example:

	macos_apps:
	- name: Sublime Text 2
	  state: present
	  domains:
	  - com.sublimetext.2
	  defaults: files/com.sublimetext.2.plist
	- name: Viscosity
	  state: absent
	  domains:
	  - com.viscosityvpn.Viscosity

### Defaults

Configure a few system defaults.
See the `macos_defaults` module for managing defaults.

| Name | Default | Description |
|------|---------|-------------|
| `macos_defaults` | [] | List of dict `{}` |

Example:

	macos_defaults:
	- domain: com.apple.screencapture
	  state: present
	  key: location
	  value: "{{ ansible_env.HOME }}/Downloads"
	  notify:
	  - macos_restart_systemuiserver
	- domain: com.apple.dock
	  state: present
	  key: tilesize
	  value: 45
	  notify:
	  - macos_restart_dock
	- domain: -g
	  state: present
	  key: QLPanelAnimationDuration
	  value: 0.0
	- domain: -g
	  state: present
	  key: NSAutomaticWindowAnimationsEnabled
	  value: no

### Paths

Lock/unlock directories (as Finder.)
See the `macos_flags` module for managing path flags.

| Name | Default | Description |
|------|---------|-------------|
| `macos_paths` | [] | list of dict `{path:,locked:<bool>}` |


FAQ
---

_Q. On uninstalling an OS/X package, I get the error `failed to uninstall package -- you might miss credentials`._

A. In that case, the .pkg was probably installed by the App Store with administrative credentials.
You'll need to build a tiny helper called `system` with `make ~/bin/system` in the localhost dir.
Then you can run `sudo system pkg com.example.Foo uninstall`.
Re-run the playbook normally afterwards.


Development
-----------

To validate the role, run `make check`.

If any of the library modules, or `macos.py`, is modified, re-compile macos by running `make files/macos`.

You can also run `make all` to do all of this above and cleanup build byproducts.
