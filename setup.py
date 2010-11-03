#!/usr/bin/env python

from distutils.core import setup

readme = open('README.md', 'rb').read()

setup(
    name = "simple-sunlight",
    version = "0.1.2",
    description = "A simpler wrapper for Sunlight's Congress API",
    long_description = readme,
    author="Chris Amico",
    author_email="eyeseast@gmail.com",
    py_modules = ['sunlight'],
    download_url = "http://github.com/eyeseast/simple-sunlight",
    url = "http://github.com/eyeseast/simple-sunlight",
)
