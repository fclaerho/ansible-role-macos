#!/usr/bin/python
# coding: utf-8
# Copyright © 2016 fclaerhout.fr — released under the MIT license.
# WANT_JSON

DOCUMENTATION = u"""
---
module: macos_app
description:
- manage macOS applications
options:
  name:
    description:
    - application name
    required: yes
  state:
    description:
    - either C(present) or C(absent)
    required: yes
"""

EXAMPLES = u"""
---
- macos_app:
    name: Sublime Text 2
    state: absent
"""

import subprocess, codecs, shutil, json, sys, os

class Dir(object):

	def __init__(self, *args):
		self.path = os.path.expanduser(os.path.join(*args))

	def exists(self):
		return os.path.exists(self.path)

	def create_if_not_exists(self):
		if not self.exists():
			os.mkdir(self.path)

	def delete_if_empty(self):
		if not os.listdir(self.path):
			os.rmdir(self.path)

class App(object):

	def __init__(self, name):
		self.name = name
		self.localdir = Dir(u"~", u"Applications")

	def __call__(self, *args):
		return subprocess.check_output(args).decode(u"utf-8")

	def get_path(self):
		u"return .app path or None"
		args = [u"find", u"/Applications"]
		if self.localdir.exists():
			args.append(self.localdir.path)
		args += [
			u"-mindepth", u"1",
			u"-maxdepth", u"2",
			u"-type", u"d",
			u"-name", u"{}.app".format(self.name)]
		stdout = self(*args)
		if not stdout:
			return None
		else:
			try:
				path, = stdout.splitlines()
				return path
			except:
				raise Exception(u"multiple matching apps found -- please report this")

	def uninstall(self):
		path = self.get_path()
		if path:
			shutil.rmtree(path)
			self.localdir.delete_if_empty()
			return True
		else:
			return False

	def install(self):
		path = self.get_path()
		if path:
			return False
		else:
			self.localdir.create_if_not_exists()
			# TODO: download from the appstore or from a given .dmg URL
			# https://github.com/fclaerho/localhost/issues/3
			raise NotImplementedError

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
	state = args[u"state"]
	name = args[u"name"]
	try:
		if state == u"present":
			changed = App(name).install()
		elif state == u"absent":
			changed = App(name).uninstall()
		else:
			raise Exception(u"{}: invalid state".format(state))
		succeed(
			changed = changed,
			state = state,
			name = name)
	except Exception as exc:
		fail(u"{}: {}".format(type(exc).__name__, exc))

if __name__ == u"__main__": main()
