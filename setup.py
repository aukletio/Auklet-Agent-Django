"""A setuptools based setup module.

See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))


def requirements(filename):
    """Reads requirements from a file."""
    with open(filename) as f:
        return [x.strip() for x in f.readlines() if x.strip()]


# Get the version from the about file.
exec(open('auklet/__about__.py').read())


setup(
    name='django-auklet',
    version=__version__,
    platforms='linux',
    packages=find_packages(),
    include_package_data=True,
    description='Auklet performance monitoring agent for Django apps',
    license='Apache',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Auklet',
    author_email='hello@auklet.io',
    url='https://github.com/aukletio/Auklet-Agent-Django',
    keywords=['iot', 'performance', 'monitoring', 'problem solving'],
    entry_points={
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Software Development :: Debuggers',
    ],
    install_requires=requirements('requirements.txt'),
    tests_require=requirements('tests.txt'),
    test_suite='tests',
)
