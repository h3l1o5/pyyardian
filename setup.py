
from setuptools import setup, find_packages

setup(
    name="pyyardian",
    version="1.0.3",
    license="MIT",
    author="Marty Sun",
    author_email="marty.sun@aeonmatrix.com",
    description="A module for interacting with the Yardian irrigation controller",
    long_description=" Python module for interacting with the Yardian irrigation controller. This module communicates directly towards the IP address of the Yardian device.",
    long_description_content_type="text/markdown",
    url="https://github.com/h3l1o5/pyyardian",
    packages=find_packages()
)