from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

long_description = """"
DataJoint Elements for Session Management
"""

with open(path.join(here, 'requirements.txt')) as f:
    requirements = f.read().splitlines()

setup(
    name='element-session',
    version='0.0.1',
    description="DataJoint Element for Session Management",
    long_description=long_description,
    author='DataJoint NEURO',
    author_email='info@vathes.com',
    license='MIT',
    url='https://github.com/datajoint/element-session',
    keywords='neuroscience session-management datajoint',
    packages=find_packages(exclude=['contrib', 'docs', 'tests*']),
    install_requires=requirements,
)
