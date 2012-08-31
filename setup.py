try:
	from setuptools import setup
except ImportError:
	from distutils.core import setup

config = {
	'description' : 'SMS Send/Receive',
	'author' : 'Wendell Philip B. Saligan',
	'url' : 'https://github.com/wends155/modem',
	'download_url' : 'https://github.com/wends155/modem',
	'author_email' : 'saliganw@gmail.com',
	'version' : '0.1',
	'install_requires' : ['pyhumod'],
	'packages' : ['modem'],
	'scripts' : [],
	'name' : 'modem'
}

setup(**config)
