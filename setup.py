#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand

class Tox(TestCommand):
    def finalize_options(self):
        command.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import tox
        errno = tox.cmdline(self.test_args)
        sys.exit(errno)

with open('requirements.txt') as reqs:
    install_requires = [
        line for line in reqs.read().split('\n') if (line and not line.startswith('--'))
        ]
setup(
    name = "hipchat-msg-parser",
    version = "0.1.0",
    description = "A simple hipchat message parser",
    long_description = "",
    packages = find_packages(exclude='tests'),
    include_package_data = True,
    entry_points = {
        'console_scripts': [
            'hipchat-msg-parse = bin.main:main'
        ],
    },
    install_requires = install_requires,
    tests_require = ['tox'],
    cmdclass = {
        'test' : Tox,
        },
)
