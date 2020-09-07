#!/usr/bin/env python

from setuptools import setup, find_packages
import os.path

setup(
    name="tap-orbit",
    version="0.0.1",
    description="Singer.io tap for extracting data from the Orbit API",
    author="Fishtown Analytics",
    url="http://fishtownanalytics.com",
    classifiers=["Programming Language :: Python :: 3 :: Only"],
    py_modules=["tap_orbit"],
    install_requires=[
        "tap-framework==0.0.4",
    ],
    entry_points="""
          [console_scripts]
          tap-orbit=tap_orbit:main
      """,
    packages=find_packages(),
    package_data={"tap_orbit": ["schemas/*.json"]},
)
