#!/usr/bin/env python
import os
try:
    from setuptools import setup
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup

description = 'Python module to manage Digitalocean droplet backups.'
long_description = description

if os.path.isfile("README.md"):
    with open('README.md') as file:
        long_description = file.read()

if os.path.isfile("LICENSE.txt"):
    with open("LICENSE.txt") as file:
        license = file.read()

setup(
    name='python-digitalocean-backup',
    version='1.1.0',
    description=description,
    author='Rob Johnson ( http://corndogcomputers.com )',
    author_email='info@corndogcomputers.com',
    url="https://github.com/corndogcomputers/python-digitalocean-backup",
    packages=['digitaloceanbackup'],
    install_requires=['python-digitalocean>=1.5'],
    download_url="https://github.com/corndogcomputers/python-digitalocean-backup/tarball/master",
    keywords=["digitalocean", "backup", "vps", "rsync", "api", "snapshot"],
    license=license,
    long_description=long_description
)
