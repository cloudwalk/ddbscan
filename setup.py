from setuptools import setup
import multiprocessing

version = '0.1.0'

install_requires = ["scipy >= 0.13.3",
                    "numpy >=1.8.1"]
tests_require = ["nose"]

setup(
    name='ddbscan',
    version=version,
    author='Allan Inocencio de Souza Costa',
    author_email='allan@cloudwalk.io',
    packages=['ddbscan'],
    license='LICENSE',
    description='Discrete DBSCAN algorithm optimized for discrete and bounded data.',
    long_description=open('README.rst').read(),
    test_suite = 'nose.collector',
    tests_require=tests_require, 
    install_requires=install_requires,
)