# The setup file
from setuptools import setup

def readme():
    with open('README.md') as f:
        return f.read()

requirements = ['time',
             'os',
             'subprocess'
                ]

setup(name='BrewPi',
version='0.0.1',
description='Brewing with Raspberry Pi',
long_description=readme(),
long_description_content_type='text/markdown',
author='FinnHeukamp',
author_email='Finn.Heukamp@t-online.de',
license='MIT',
keywords='core package',
packages=['BrewPi'],
#install_requires=requirements,
include_package_data=True,
zip_safe=False
      )