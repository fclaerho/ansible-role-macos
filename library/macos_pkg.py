#!/usr/bin/python
# coding: utf-8
# Copyright © 2016 fclaerhout.fr — released under the MIT license.
# WANT_JSON

DOCUMENTATION = u"""
---
module: macos_pkg
description:
- manage macOS packages
options:
  name:
    description:
    - package id
    default: no
  state:
    description:
    - either C(present) or C(absent)
    default: no
"""

EXAMPLES = u"""
---
- macos_pkg:
    name: com.example.Foo
    state: absent
"""

import subprocess, codecs, json, sys, os

class Pkgutil(object):

	def __call__(self, *args):
		return subprocess.check_output(args).decode(u"utf-8")

	def list(self):
		return sorted(self(u"pkgutil", u"--packages").splitlines())

	def is_installed(self, name):
		return name in self.list()

	def install(self, name):
		if self.is_installed(name):
			return False
		else:
			raise NotImplementedError

	def uninstall(self, name, interactive = True):
		if self.is_installed(name):
			# fetch package installation directory:
			info = {}
			for line in self(u"pkgutil", u"--pkg-info", name).splitlines():
				key, value = line.split(":")
				info[key.strip()] = value.strip()
			dirname = os.path.join(info[u"volume"], info[u"location"])
			# fetch file list:
			stdout = self(u"pkgutil", u"--files", name)
			paths = tuple(os.path.join(dirname, line) for line in stdout.splitlines())
			# ask user for confirmation:
			if interactive:
				print "\n".join(paths)
				if raw_input(u"Proceed (y/n)? ") != u"y": return
			# delete files first...
			for path in filter(os.path.isfile, paths):
				if os.path.exists(path):
					os.remove(path)
			# ...then delete *empty* directories
			for path in sorted(filter(os.path.isdir, paths), reverse = True):
				if os.path.exists(path):
					if not os.listdir(path):
						os.rmdir(path)
					else:
						sys.stderr.write(u"{}: skipping non-empty directory\n".format(path))
			self(u"pkgutil", u"--forget", name)
			assert not self.is_installed(name), u"failed to uninstall package -- you might miss credentials"
			return True
		else:
			return False

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
	name = args[u"name"]
	state = args[u"state"]
	pkgutil = Pkgutil()
	try:
		if args[u"state"] == u"present":
			changed = Pkgutil().install(name)
		elif args[u"state"] == u"absent":
			changed = Pkgutil().uninstall(
				name = name,
				interactive = False)
		else:
			raise Exception(u"{}: invalid state".format(state))
		succeed(
			changed = changed,
			state = state,
			name = name)
	except Exception as exc:
		fail(u"{}: {}".format(type(exc).__name__, exc))

if __name__ == u"__main__": main()
