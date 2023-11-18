#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import setuptools
import os

NAME = 'pon2'
VERSION = "1.0"
AUTHOR = 'Noverdo-Gagarinten'
EMAIL = 'thefinalspacestudio@gmail.com'
DESCRIPTION = 'PON/2 - Python Object Notation, JSON with python types and Custom Classes'
URL = 'https://github.com/noverd/PON2/'
REQUIRES_PYTHON = '>=3.12.0'
REQUIRED = ["sly"]
README = 'README.rst'


here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, README), "r") as fp:
    long_description = fp.read()

setuptools.setup(
    name="pon2",
    version=VERSION,
    author=AUTHOR,
    author_email=EMAIL,
    description=DESCRIPTION,
    long_description=long_description,
    url=URL,
    packages=["pon2"],
    python_requires=REQUIRES_PYTHON,
    install_requires=REQUIRED,
    classifiers=[
        "Programming Language :: Python :: 3",
        'Programming Language :: Python :: 3.12',
        "Operating System :: OS Independent",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering"
    ]
)
