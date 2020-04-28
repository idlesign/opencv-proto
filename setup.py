import io
import os
import re

from setuptools import setup, find_packages

import sys

PATH_BASE = os.path.dirname(__file__)


def read_file(fpath):
    """Reads a file within package directories."""
    with io.open(os.path.join(PATH_BASE, fpath)) as f:
        return f.read()


def get_version():
    """Returns version number, without module import (which can lead to ImportError
    if some dependencies are unavailable before install."""
    contents = read_file(os.path.join('ocvproto', '__init__.py'))
    version = re.search('VERSION = \(([^)]+)\)', contents)
    version = version.group(1).replace(', ', '.').strip()
    return version


DEPS = [
    'opencv-python',
    'colorhash',
]

setup(
    name='opencv-proto',
    version=get_version(),
    url='https://github.com/idlesign/opencv-proto',

    description='Allows fast prototyping in Python for OpenCV',
    long_description=read_file('README.rst'),
    license='BSD 3-Clause License',

    author='Igor `idle sign` Starikov',
    author_email='idlesign@yandex.ru',

    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    zip_safe=False,

    install_requires=[],
    setup_requires=(['pytest-runner'] if 'test' in sys.argv else []),

    extras_require={
        'all':  DEPS,
    },

    test_suite='tests',
    tests_require=[
        'pytest',
        'pytest-stub>=1.1.0',
    ] + DEPS,

    classifiers=[
        # As in https://pypi.python.org/pypi?:action=list_classifiers
        'Development Status :: 4 - Beta',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'License :: OSI Approved :: BSD License',
    ],
)


