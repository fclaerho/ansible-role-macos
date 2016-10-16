# coding: utf-8
# Copyright © 2016 fclaerhout.fr, released under the MIT license.

"""
macOS system management helper.

Usage:
  __TGTNAME__ [options] pkg [NAME [uninstall]]

Options:
  -f, --force  run without prompting for confirmation
  -h, --help   output this help message and exit
"""

import macos_defaults
import macos_flags
import macos_app
import macos_pkg
import docopt

def print_list(obj):
	for item in obj:
		print item

def main(args = None):
	opts = docopt.docopt(
		doc = __doc__,
		argv = args,
		version = "0.1-__BUILDHASH__")
	try:
		if opts["pkg"]:
			pkgutil = macos_pkg.Pkgutil()
			if opts["NAME"]:
				if opts["uninstall"]:
					pkgutil.uninstall(
						name = opts["NAME"],
						interactive = opts["--force"])
				else:
					raise NotImplementedError
			else:
				print_list(pkgutil.list())
		else:
			raise NotImplementedError
	except Exception as exc:
		raise SystemExit("{}: {}".format(type(exc).__name__, exc))

if __name__ == "__main__": main()
