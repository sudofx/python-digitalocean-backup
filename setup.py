#!/usr/bin/env python
import os
try:
    from setuptools import setup
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup

long_description = """A python package that works with python-digitalocean to rsync and snapshot your droplets."""

if os.path.isfile("README.md"):
    with open('README.md') as file:
        long_description = file.read()

setup(
    name='python-digitalocean-backup',
    version='0.0.1',
    description='digitalocean.com droplet rsync and snapshot',
    author='Rob Johnson ( http://corndogcomputers.com )',
    author_email='info@corndogcomputers.com',
    packages=['backdroplet'],
    install_requires=['python-digitalocean'],
    long_description=long_description
)