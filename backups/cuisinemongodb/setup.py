try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
from cuisinemongodb import __version__, __maintainer__, __email__


license_text = open('LICENSE.txt').read()
long_description = open('README.rst').read()


setup(
    author = __maintainer__,
    author_email = __email__,
    classifiers = [
        'Programming Language :: Python',
        'Development Status :: 3 - Alpha',
        'Natural Language :: English',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Topic :: Utilities',
    ],
    data_files=[('', ['AUTHORS', 'LICENSE.txt', 'README.rst'])],
    description = 'Cuisine methods for MonoDB',
    install_requires = ['cuisine', 'fabric'],
    license = license_text,
    long_description=long_description,
    name = 'cuisine-postgresql',
    py_modules = ['cuisine_postgresql'],
    url = 'http://github.com/josepato/cuisine-mongodb',
    version = __version__,
)
