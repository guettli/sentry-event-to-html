import setuptools
from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='sentry-event-to-html',

    # Updated via travisd: https://travis-ci.org/guettli/sentry-event-to-html
    # See .travis.yml
    version='2018.1.0',

    description='sentry-event-to-html: Create HTML from a sentry event',
    long_description=long_description,

    url='https://github.com/guettli/sentry-event-to-html/',

    author='Thomas Guettler',
    author_email='info.sentry-event-to-html@thomas-guettler.de',

    license='Apache Software License 2.0',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 5 - Production/Stable',

        # Indicate who your project is intended for
        'Intended Audience :: Information Technology',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: Apache Software License',


        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
    ],

    install_requires=[
        'sentry-sdk',
    ],
    packages=setuptools.find_packages(),

)
