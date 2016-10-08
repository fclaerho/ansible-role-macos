
![Ansible Logo](ansible-logo.png)

This Ansible role brings macOS modules to manage apps, defaults, flags, and packages.
It is primarily designed for a local user, in order to setup a work environment.

Variables
=========

Apps
----

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

Defaults
--------

Configure a few system defaults.
See the `macos_defaults` module for managing defaults.

| Name | Default | Description |
|------|---------|-------------|
| `macos_screencapture_path` | false | Set the screenshot storage location |
| `macos_animations` | true ||
| `macos_dock_size` | false ||


Paths
-----

Lock/unlock directories.
See the macos_flags module for managing path flags.

| Name | Default | Description |
|------|---------|-------------|
| `macos_paths` | [] | list of dict `{path:,locked:<bool>}` |

Development
===========

Run `make check` to validate the role.
