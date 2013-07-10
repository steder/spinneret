#!/usr/bin/env python

import os

from setuptools import find_packages
from setuptools import setup


with open("requirements.txt", "r") as requirements_file:
    requirements = [req.strip() for req in requirements_file.read().split("\n")]


ROOT = os.path.dirname(__file__)


def version():
    init = os.path.join(ROOT, "spinneret", "__init__.py")
    version = None
    for line in open(init, "r"):
        if line.startswith("__version__"):
            version = line.split("=")[-1].strip().replace('\"', '')
    assert version is not None, "Unable to determine version!"
    return version


def long_description():
    readme = os.path.join(ROOT, "README.rst")
    long_description = open(readme, "r").read()
    return long_description


setup(name='spinneret',
      author="Mike Steder",
      author_email="steder@gmail.com",
      version=version(),
      description='Quick web spider and traffic generator',
      packages=find_packages(),
      package_data={'': ['config/*']},
      scripts=["bin/spinneret",],
      test_suite='nose.collector',
      install_requires=requirements,
      classifiers=["Development Status :: 3 - Alpha",
                   "Programming Language :: Python",
                   "Programming Language :: Python :: 2",
                   "Programming Language :: Python :: 2.7",
                   "Topic :: Utilities",],
      url="https://github.com/steder/spinneret",
      long_description=long_description(),
)
