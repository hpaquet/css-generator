from os import path
import runpy
from setuptools import setup

version_meta = runpy.run_path("./css_generator/_version.py")
VERSION = version_meta["__version__"]

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='css-generator',
    version=VERSION,
    author='Hugo Paquet',
    packages=['css_generator'],
    include_package_data=True,
    license='MIT',
    description='CSS stylesheet generator',
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=[],
    classifiers=[
    ],    
)
