#!/usr/bin/python
# coding: utf-8
# Copyright © 2016 fclaerhout.fr — released under the MIT license.
# WANT_JSON

DOCUMENTATION = u"""
---
module: macos_defaults
description:
- manage macOS domain defaults
options:
  domain:
    description:
    - domain name
    required: no
    default: -g
  state:
    description:
    - either C(present) or C(absent)
    - if key is defined, write/delete the key
    - if key is undefined, import/delete the domain
    required: yes
  path:
    description:
    - required if state=present and key is undefined
    - path to a plist file
    required: no
  key:
    description:
    - key associated to the domain.
    required: no
  value:
    description:
    - required if state=present and key is defined
    - the actual value type is the same than the YAML type
    required: no
"""

EXAMPLES = u"""
---
- macos_defaults:
    domain: com.apple.Dock
    state: present
    key: tilesize
    value: 45
- macos_defaults:
    domain: com.apple.Xcode
    state: present
    path: /tmp/com.apple.Xcode.plist
"""

import subprocess, tempfile, filecmp, codecs, shutil, json, sys, os

def Path(*args):
	return os.path.expanduser(os.path.join(*args))

class Defaults(object):

	def __call__(self, *args):
		return subprocess.check_output(args).decode(u"utf-8")

	def __init__(self, domain):
		self.domain = domain

	def exists(self):
		return self.domain in self(u"defaults", u"domains").strip().split(u", ")

	def create(self, path):
		u"import defaults from path if differing and return True, return False otherwise"
		if os.path.dirname(path) == Path(u"~", u"Library", u"Preferences"):
			return False
		with tempfile.NamedTemporaryFile() as fp:
			self(u"defaults", u"export", self.domain, fp.name)
			if filecmp.cmp(path, fp.name):
				return False
		self(u"defaults", u"import", self.domain, path)
		return True

	def purge(self):
		u"delete defaults if any and return True, return False otherwise"
		if self.exists():
			filename = u"{}.plist".format(self.domain)
			paths = (
				Path(u"~", u"Library", u"Preferences", filename),
				Path(u"~", u"Library", u"Containers", self.domain, u"Data", u"Library", u"Preferences", filename))
			paths = filter(os.path.exists, paths)
			for path in paths:
				os.remove(path)
			assert not self.exists(), u"oops, defaults still exist after purge"
			return True
		else:
			return False

	def write(self, key, value):
		u"write key if differing and return True, return False otherwise"
		if self.exists():
			if key in self(u"defaults", u"read", self.domain):
				current_value = self(u"defaults", u"read", self.domain, key).strip()
				_, current_type = self(u"defaults", u"read-type", self.domain, key).strip().split(u" is ")
				if current_type == u"boolean":
					current_value = False if current_value == u"0" else True
				elif current_type == u"string":
					current_value = current_value.decode(u"utf-8")
				elif current_type == u"integer":
					current_value = int(current_value)
				elif current_type == u"float":
					current_value = float(current_value)
				else:
					raise Exception(u"{}: unsupported type on reading".format(current_type))
				if current_value == value:
					return False
				#else: # uncomment to debug
				#	raise Exception("{} != {}".format(current_value, value))
		args = [u"defaults", u"write", self.domain, key]
		if isinstance(value, bool):
			args += [u"-bool", u"true" if value else u"false"]
		elif isinstance(value, unicode):
			args += [u"-string", value.encode(u"utf-8")]
		elif isinstance(value, int):
			args += [u"-int", u"{}".format(value)]
		elif isinstance(value, float):
			args += [u"-float", u"{}".format(value)]
		else:
			raise Exception(u"{}: unsupported type on writing".format(type(value).__name__))
		self(*args)
		return True

	def delete(self, key):
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
	domain = args.get(u"domain", u"-g")
	state = args[u"state"]
	key = args.get(u"key", None)
	try:
		if key:
			if state == u"present":
				changed = Defaults(domain).write(key, args[u"value"])
			elif state == u"absent":
				changed = Defaults(domain).delete(key)
			else:
				raise Exception(u"{}: invalid state".format(state))
			succeed(
				changed = changed,
				domain = domain,
				state = state,
				key = key)
		else:
			if state == u"present":
				path = Path(args[u"path"])
				changed = Defaults(domain).create(path)
			elif state == u"absent":
				changed = Defaults(domain).purge()
			else:
				raise Exception(u"{}: invalid state".format(state))
			succeed(
				changed = changed,
				domain = domain,
				state = state)
	except Exception as exc:
		fail(u"{}: {}".format(type(exc).__name__, exc))

if __name__ == u"__main__": main()
