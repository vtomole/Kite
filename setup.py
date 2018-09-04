#!/usr/bin/python

from setuptools import setup

setup(
    name="kite",
    author="qchackers",
    url="https://github.com/QCHackers/kite.git",
    description="Quantum Programming library in Python",
    packages=[
        "kite",
        "eagle",
    ],
    install_requires=[
        "numpy >= 1.14",
    ],
)
