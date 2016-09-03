#!/usr/bin/env python

from setuptools import setup
setup(
    install_requires=['autobahn'],
    tests_require=['pytest'],
    setup_requires=['pbr>=1.9', 'setuptools>=17.1','pytest-runner'],
    pbr=True,
)

# import os
# from setuptools import setup, find_packages

# import flybywire
# # Utility function to read the README file.
# # Used for the long_description.  It's nice, because now 1) we have a top level
# # README file and 2) it's easier to type in the README file than to put a raw
# # string in below ...
# def read(fname):
#     return open(os.path.join(os.path.dirname(__file__), fname)).read()
#
# setup(
#     name = "flybywire",
#     version = flybywire.__version__,
#     author = "Thomas Antony",
#     author_email = "tantony.purdue@gmail.com",
#
#     description = "A library for building virtual-DOM user interfaces in pure Python.",
#     long_description=read('README.md'),
#
#     license = "MIT",
#     keywords = ['react', 'web framework', 'javascript',
#                 'asynchronous', 'gui', 'websockets'],
#
#     url = "https://github.com/thomasantony/flybywire",
#     packages = find_packages(),
#     package_data = {
#         'flybywire': ['static/main.html', 'static/flybywire.js']
#     },
#
#     install_requires=['autobahn'],
#     setup_requires=['pbr>=1.9','setuptools>=17.1','pytest-runner'],
#     tests_require=['pytest'],
#     pbr=True,
#     classifiers=[
#         "Development Status :: 2 - Pre-Alpha",
#         "Topic :: Software Development :: Libraries",
#         "Intended Audience :: Developers",
#         "Programming Language :: Python",
#         "Programming Language :: Python :: 2.7",
#         "Programming Language :: Python :: 3.4",
#         "Programming Language :: Python :: 3.5",
#         "License :: OSI Approved :: MIT License",
#     ],
#
# )
