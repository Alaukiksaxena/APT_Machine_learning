#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
compositionspace : add licence and such
"""

from setuptools import setup, find_packages, Extension

with open('README.md') as readme_file:
    readme = readme_file.read()

setup_requirements = ['pytest-runner', ]
test_requirements = ['pytest>=3', ]

setup(
    author="Alaukik Saxena, Sarath Menon, Mariano Forti",
    author_email='s.menon@mpie.de',
    python_requires='>=3.8',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    description="APT analysis tools",
    install_requires = ['numpy', 'matplotlib', 'pandas', 'h5py', 'scikit-learn',
    'tqdm', 'pyevtk', 'pyyaml', 'pyvista'],
    #license="GNU General Public License v3",
    long_description=readme,
    long_description_content_type='text/markdown',
    include_package_data=True,
    keywords='compositionspace',
    name='compositionspace',
    packages=find_packages(include=['compositionspace', 'compositionspace.*']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='',
    version='0.0.9',
    zip_safe=False,
    #entry_points={
    #    'console_scripts': [
    #        'calphy = calphy.kernel:main',
    #        'calphy_kernel = calphy.queuekernel:main',
    #    ],
    #}
)

