import setuptools
import os

with open("README.md", "r") as fh:
    long_description = fh.read()

PACKAGE_EXCLUDE = [
    "tests",
    "project",
    "*pytest*"
    "test"
]

SETUP_REQS = [
    "setuptools >= 40.5.0",
    "wheel >= 0.32.2"
]

TEST_REQS = [
    "pytest >= 3.7.2",
    "pep8 >= 1.7.1"
]


setuptools.setup(
    name="elasticsearchpy",
    version="0.0.1",
    author="koebane82",
    author_email="jeff@koebane.net",
    description="A python ElasticSearch Library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/koebane82/elasticsearchpy",
    packages=setuptools.find_packages(exclude=PACKAGE_EXCLUDE),
    classifiers=[
        "License :: GNU General Public License v3.0",
        "Operating System :: OS Independent",
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    setup_requires=SETUP_REQS,
    tests_require=TEST_REQS
)
