
<img alt="Ansible Logo" src="ansible-logo.png" align="right" />

_This [Ansible role](https://docs.ansible.com/playbooks_roles.html) brings macOS modules to manage apps, defaults, flags, and packages. It is primarily designed for a local user, to setup a work environment._

[Usage](#usage) | [Variables](#variables) | [Development](#development)

Usage
-----

You can use this role in a playbook or as the dependency of another role.

To be completed.

<!--
In a playbook:
add the Galaxy ID or repository URL to the requirements file,
then call `ansible-galaxy install -r $REQUIREMENTS`,
or you can use it as another **role dependency**,
by adding its ID in the `dependencies` list of the role manifest `meta/main.yml`.
The **stable version** of this role is registered on Galaxy with the ID `fclaerho.syskit`;
you can alternatively use this repository URL as ID for the **development version**.
-->

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

Dependencies
------------

None.

Development
-----------

Run `make check` to validate the role.
