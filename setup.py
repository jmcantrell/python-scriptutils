#!/usr/bin/env python

from setuptools import setup, find_packages
from glob import glob

setup(
        name='ScriptUtils',
        version='0.4.1',
        description='Various small utilities for use in other scripts.',
        author='Jeremy Cantrell',
        author_email='jmcantrell@gmail.com',
        classifiers=[
            'Development Status :: 3 - Alpha',
            'Environment :: Console',
            'Intended Audience :: Developers',
            'License :: OSI Approved :: GNU General Public License (GPL)',
            'Natural Language :: English',
            'Operating System :: OS Independent',
            'Programming Language :: Python',
            ],
        packages=[
            'scriptutils',
            ],
        install_requires=[
            'UnicodeUtils>=0.2',
            ],
        )
