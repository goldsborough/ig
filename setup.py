#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
setup.py script for setuptools.
"""

import re

from setuptools import setup, find_packages

with open('ig/__init__.py') as init:
    text = init.read()
    match = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', text, re.M)
    version = match.group(1)

with open('README.md') as readme:
    long_description = readme.read()

setup(
    name='ig-cpp',
    version=version,

    description='A tool to visualize include graphs for C++ projects',
    long_description=long_description,

    url="https://github.com/goldsborough/ig",
    license='MIT',

    author='Peter Goldsborough',
    author_email='peter@goldsborough.me',

    classifiers=[
        'Development Status :: 5 - Production/Stable',

        'Intended Audience :: Developers',
        'Topic :: Software Development',

        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5'
    ],
    keywords='visualization C++ tool',
    packages=find_packages(exclude=['www']),
    include_package_data=True,
    package_data=dict(ig=[
        '../README.md',
        '../Makefile',
        '../www/*',
        '../www/sigma/*'
    ]),

    entry_points=dict(console_scripts=['ig = ig.main:main'])
)
