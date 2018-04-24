from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='await_ccb',
    version='0.1.1',
    description='Waits for Google Cloud Container Build to complete',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Reid Beels',
    author_email='reid@thedyrt.com',
    url='https://github.com/thedyrt/await-ccb',
    license='MIT',
    keywords='google cloud container builder',
    packages=find_packages(),
    install_requires=[
        'google-auth',
        'google-auth-httplib2',
        'google-api-python-client',
        'docopt'
    ],
    entry_points={
        'console_scripts': ['await-ccb=await_ccb.cli:main']
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6'
    ],
)
