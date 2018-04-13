#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ts=4:sw=4
# GPLv3 or later, Dirk Sohler
# http://dev.0x7be.de/mkpassword.html


import re
import string
import random

from optparse import OptionParser
from pprint import pprint as pp

progversion='2.0.1'

def options():
	parser = OptionParser()
	parser = OptionParser(
			usage='%prog [options]',
			version='%prog '+progversion)
	parser.add_option('-v', '--verbose',
			action='store_true',
			default=False,
			dest='verbose',
			help='Verbose output')
	parser.add_option('-l', '--length',
			default=20,
			dest='length',
			metavar='N',
			help='password lenght in characters')
	parser.add_option('-s', '--salt',
			default=False,
			dest='salt',
			metavar='X',
			help='use X as salt')
	parser.add_option('-c', '--config-secure',
			action='store_true',
			default=False,
			dest='configsecure',
			help='skip some problematic characters')
	parser.add_option('-n', '--no-colors',
			action='store_true',
			default=False,
			dest='nocolors',
			help='don’t use colored output')
	parser.add_option('-a', '--alpha-numeric',
			action='store_true',
			default=False,
			dest='alnum',
			help='only use letters and numbers')
	parser.add_option('-q', '--quiet',
			action='store_true',
			default=False,
			dest='quiet',
			help='only output the password')
	return parser
params = options()
options,urls = params.parse_args()


def cprint(text):
	# http://blog.holloway-web.de/wp-content/uploads/2009/11/ansi_colors.png
	if not options.nocolors == True:
		regular = {'gray': '\033[0;30m', 'red':  '\033[0;31m',
				'green': '\033[0;32m', 'yellow': '\033[0;33m',
				'dblue': '\033[0;34m', 'purple': '\033[0;35m',
				'lblue': '\033[0;36m', 'white': '\033[0;37m'
				}
		bold = {'gray': '\033[1;30m', 'red':  '\033[1;31m',
				'green': '\033[1;32m', 'yellow': '\033[1;33m',
				'dblue': '\033[1;34m', 'purple': '\033[1;35m',
				'lblue': '\033[1;36m', 'white': '\033[1;37m'
				}
		def rc(o): return regular[o.group(1).lower()]
		def bc(o): return bold[o.group(1).lower()]
		text = text.replace('|RESET|', '\033[0m') # reset in text
		text += '\033[0m' # reset at EOL
		text = re.sub('\|([a-z]{3,6})\|',rc, text) # regular colors
		text = re.sub('\|([A-Z]{3,6})\|',bc, text) # bold colors
	else:
		text = re.sub('\|([A-Za-z]{3,6})\|','', text)
	print(text)


def info(text):
	if not options.quiet:
		cprint(text);


def verbose(text):
	if options.verbose == True:
		cprint('|GRAY|[%s]' % text)


def showoption(opt, vinfo, text):
	verbose('checking %s to be set' % vinfo)
	if opt != False:
		info(' |LBLUE|-> |PURPLE|%s' % text)


def genpassword():
	verbose('Generating password')
	if options.salt != False:
		verbose('Adding salt %s' % str(options.salt))
		salt = str(options.salt)
	else:
		salt = ''

	chars = string.ascii_letters + string.digits

	if options.alnum != True:
		chars += string.punctuation

	base = ''.join(random.choice(chars + salt)
			for x in range(int(options.length)))

	if options.configsecure == True:
		verbose('Filtering characters for config security')
		base = base.replace('\\', '').replace('\'', '').replace('\"', '')
		if len(base) < int(options.length):
			diff = int(options.length) - len(base)
			if diff == 1:
				char = 'character'
			else:
				char = 'characters'
			cprint(('|YELLOW| -> |PURPLE|Removed |DBLUE|%i '+
					'|PURPLE|%s (config-secure)')
					% (diff, char))
	
	return base


def main():

	info('|WHITE|Generating password')

	verbose('Calculating password security')
	if int(options.length) < 10:
		length = '|RED|%s' % options.length
		quality = 'low'
	elif int(options.length) < 20:
		length = '|YELLOW|%s' % options.length
		quality = 'average'
	elif int(options.length) > 100:
		length = '|GREEN|%s' % options.length
		quality = 'RU SRS? *g*'
	else:
		length = '|GREEN|%s' % options.length
		quality = 'good'

	showoption(length, 'length', 'Length of %s |PURPLE|characters (%s)'
			% (length,quality))
	showoption(options.configsecure, 'config security',
			'Config secure (no |DBLUE|\\|PURPLE|, '+
			'|DBLUE|\'|PURPLE|, and |DBLUE|"|PURPLE|)')
	showoption(options.alnum, 'alpha-numeric', 'Only with letters and numbers')
	showoption(options.salt, 'salt', 'With salt |DBLUE|%s' % options.salt)

	password = genpassword()
	verbose('Printing password')
	cprint('|WHITE|%s' % password)



if __name__ == '__main__':
    main()
