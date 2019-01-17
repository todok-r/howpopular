#!/usr/bin/env python

from setuptools import setup, find_packages
import howpopular
import os


def extra_dependencies():
    import sys
    return ['argparse'] if sys.version_info < (2, 7) else []


def read(*names):
    values = dict()
    for name in names:
        value = ''
        for extension in ('.txt', '.rst'):
            filename = name + extension
            if os.path.isfile(filename):
                with open(filename) as in_file:
                    value = in_file.read()
                break
        values[name] = value
    return values


long_description = """
%(README)s

News
====

%(CHANGES)s

""" % read('README', 'CHANGES')

setup(
    name='howpopular',
    version=howpopular.__version__,
    description='command line popularity checker',
    long_description=long_description,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Topic :: Documentation",
    ],
    keywords='howpopular help console command line answer',
    author='todok-r',
    maintainer='todok-r',
    url='https://github.com/todok-r/howpopular',
    license='MIT',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'howpopular = howpopular.howpopular:command_line_runner',
        ]
    },
    install_requires=[
        'pyquery',
        'requests',
        'requests-cache'
    ] + extra_dependencies(),
)
