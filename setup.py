import setuptools

with open("README.md", "r") as fh:
    long_description = rh.read()

setuptoos.setup(
    name="elasticsearchpy",
    version="0.0.1",
    author="koebane82",
    author_email="jeff@koebane.net",
    description="A python ElasticSearch Library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/koebane82/elasticsearchpy",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: GNU General Public License v3.0",
        "Operating System :: OS Independent"
    ]
)
