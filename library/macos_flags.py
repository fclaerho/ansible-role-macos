#!/usr/bin/python
# coding: utf-8
# Copyright © 2016 fclaerhout.fr — released under the MIT license.
# WANT_JSON

DOCUMENTATION = u"""
---
module: macos_flags
description:
- manage macOS file flags
options:
  path:
    description:
    - file path
    required: yes
  archived:
    description:
    - boolean
    - archived flag (super-user only)
    required: no
  opaque:
    description:
    - boolean
    - opaque flag (owner or super-user only)
    - directory is opaque when viewed through a union mount
    required: no
  dump:
    description:
    - boolean
    required: no
  sappend:
    description:
    - boolean
    - set the system append-only flag (super-user only)
    - may only be unset when the system is in single-user mode
    required: no
  schange:
    description:
    - boolean
    - set the system immutable flag (super-user only)
    - may only be unset when the system is in single-user mode
    required: no
  uappend:
    description:
    - boolean
    - set the user append-only flag (owner or super-user only)
    required: no
  uchange:
    description:
    - boolean
    - set the user immutable flag (owner or super-user only)
    required: no
  hidden:
    description:
    - boolean
    - hide item from GUI
    required: no
"""

EXAMPLES = u"""
---
- macos_flags:
    path: ~/Public
    uchange: yes
"""

import subprocess, codecs, json, sys, os

def get_flags(path):
	# man chflags:
	# You can use "ls -lO" to see the flags of existing files.
	stdout = subprocess.check_output([u"ls", u"-dlO", path]).decode(u"utf-8")
	_, _, _, _, value, _, _, _, _, _ = stdout.splitlines()[0].split()
	return value.split(u",") if value != u"-" else ()

def set_flags(path, flags):
	subprocess.check_call([u"chflags", u"-LR", u",".join(flags), path])

ALIASES = {
	u"archived": [u"arch"],
	u"opaque": [],
	u"dump": [],
	u"sappend": [u"sappnd"],
	u"schange": [u"schg", u"simmutable"], # system immutable
	u"uappend": [u"uappnd"],
	u"uchange": [u"uchg", u"uimmutable"], # user immutable
	u"hidden": [],
}

# from manpage:
# Putting/removing the letters "no" before/from a keyword causes the flag to be cleared.
def normalized(flags):
	u"normalize a list of flags"
	result = []
	for item in flags:
		if item.startswith(u"no"):
			negated = True
			item = item[2:]
		else:
			negated = False
		if item in ALIASES: # is it a basename?
			flag = item
		else:
			for key in ALIASES:
				if item in ALIASES[key]: # is it an alias?
					flag = key
					break
			else:
				raise KeyError(u"{}: no such flag".format(item))
		result.append(u"no{}".format(flag) if negated else flag)
	return result

def succeed(changed, **kwargs):
	kwargs.update({u"changed": changed})
	print json.dumps(kwargs)
	raise SystemExit

def fail(msg):
	print json.dumps({
		u"failed": True,
		u"msg": msg,
	})
	raise SystemExit(1)

def main():
	if len(sys.argv) < 2:
		raise SystemExit(u"usage: {} <path>".format(sys.argv[0]))
	with codecs.open(sys.argv[1], encoding = u"utf-8") as fp:
		args = json.load(fp)
	path = os.path.expanduser(args[u"path"])
	flags = []
	for key in ALIASES:
		if key in args:
			flags.append(key if args[key] else u"no{}".format(key))
	try:
		if set(normalized(get_flags(path))) == set(flags):
			changed = False
		else:
			changed = True
			set_flags(
				path = path,
				flags = flags)
		succeed(
			changed = changed,
			flags = flags,
			path = path)
	except Exception as exc:
		fail(u"{}: {}".format(type(exc).__name__, exc))

if __name__ == u"__main__": main()
