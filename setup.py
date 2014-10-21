from setuptools import setup
import multiprocessing

version = '0.2.4'

install_requires = ["scipy >= 0.13.3",
                    "numpy >=1.8.1"]

tests_require = ["nose"]

classifiers=[
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3.3',
    'Topic :: Scientific/Engineering :: Artificial Intelligence',
]

setup(
    name='ddbscan',
    version=version,
    author='Allan Inocencio de Souza Costa',
    author_email='allan@cloudwalk.io',
    url='https://github.com/cloudwalkio/ddbscan',
    packages=['ddbscan'],
    license='MIT',
    description='Discrete DBSCAN algorithm optimized for discrete and bounded data.',
    long_description=open('README.rst').read(),
    test_suite = 'nose.collector',
    tests_require=tests_require,
    install_requires=install_requires,
    classifiers=classifiers,
)
