#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8

"""
"""
from setuptools import setup, find_packages

setup(
    name='fundata-varena',
    version='0.0.1',
    description='A fundata sdk package for api.varena.com, \
            for API docs, see http://open.varena.com/',
    license='MIT',
    packages=find_packages(),
    package_dir = {},
    author='VArena Shanghai Team',
    author_email='fundata@varena.com',
    keywords=['fundata', 'varena'],
    install_requires=[],
    url='https://github.com/fundata-varena/fundata-python-sdk'
)
