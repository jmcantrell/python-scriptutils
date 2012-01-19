#!/usr/bin/env python

from setuptools import setup

setup(
        name='ScriptUtils',
        version='0.9.1',
        description='Various utilities for use in other scripts.',
        author='Jeremy Cantrell',
        author_email='jmcantrell@gmail.com',
        classifiers=[
            'Development Status :: 4 - Beta',
            'Environment :: Console',
            'Intended Audience :: Developers',
            'License :: OSI Approved :: BSD License',
            'Natural Language :: English',
            'Operating System :: OS Independent',
            'Programming Language :: Python',
            ],
        packages=[
            'scriptutils',
            ],
        install_requires=[
            'PathUtils',
            'UnicodeUtils',
            ],
        )
