
<img alt="Ansible Logo" src="https://github.com/fclaerho/ansible-role-macos/blob/master/ansible-logo.png" align="right" />

_This [Ansible role](https://docs.ansible.com/playbooks_roles.html) brings macOS modules to manage apps, defaults, flags, and packages. It is primarily designed for a local user, to setup a work environment._

[![Build Status](https://travis-ci.org/fclaerho/ansible-role-macos.svg?branch=master)](https://travis-ci.org/fclaerho/ansible-role-macos)

[Usage](#usage) | [Variables](#variables) | [Development](#development)


Usage
-----

You can use this role in a playbook or as another role's dependency.

With a playbook:
- add the Galaxy ID or repository URL to your requirements
- run `ansible-galaxy install -r …` to install requirements
- call the role from a `roles:` clause in a play

As another role's dependency:
- add the Galaxy ID or repository URL to the `dependencies:` list of the role manifest `meta/main.yml`
- roles dependencies are always executed before the role that includes them


Variables
---------

### Apps

Restore (state: present) or purge (state: absent) an app.

Restoring an app does not support a full install and is primarily designed for restoring a configuration.

NOTICE! Purging an app includes its defaults, preferences, support, container and package. Make sure to have a backup of your application defaults beforehands.

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
| `macos_screencapture_path` | false | Set the path to store screenshots |
| `macos_animations` | true ||
| `macos_dock_size` | false ||


### Paths

Lock/unlock directories (as Finder.)
See the macos_flags module for managing path flags.

| Name | Default | Description |
|------|---------|-------------|
| `macos_paths` | [] | list of dict `{path:,locked:<bool>}` |


Development
-----------

Run `make check` to validate the role.
