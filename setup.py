#!/usr/bin/python3

from setuptools import find_packages, setup

with open("README.md", "r") as fh:
    long_description = fh.read()

with open("requirements.txt", "r") as f:
    requirements = list(map(str.strip, f.read().split("\n")))[:-1]

setup(
    name="dutchswap",
    packages=find_packages(),
    version="0.0.7",  # don't change this manually, use bumpversion instead
    license="MIT",
    description="A framework for digital dutch auctions",  # noqa: E501
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Adrian Guerrera",
    author_email="adrian@deepyr.com",
    url="https://github.com/deepyr/dutchswap",
    keywords=["dutchswap"],
    install_requires=requirements,
    include_package_data=True,
    python_requires=">=3.6,<4",
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
)
