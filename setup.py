import os
from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name='memo',
    version='0.0.0',
    author='wanshot',
    author_email='',
    description='',
    license='MIT',
    keywords='',
    long_description=read('README.rst'),
    classifiers=[
        'License :: OSI Approved :: MIT License',
    ],
    packages=['memo'],
    entry_points={
        'console_scripts': ['memo = memo.run:main']
    },
    install_requires=['argparse', 'six', 'wcwidth'],
)
