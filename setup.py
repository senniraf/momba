# -*- coding:utf-8 -*-
#
# Copyright (C) 2019, Maximilian Köhl <mkoehl@cs.uni-saarland.de>

from __future__ import annotations

from distutils.core import setup


setup(
    name='momba',
    version='0.0.1dev',
    description='A Python library for quantitative models.',
    author='Maximilian Köhl',
    author_email='mkoehl@cs.uni-saarland.de',
    url='https://dgit.cs.uni-saarland.de/koehlma/momba',

    setup_requires=['pytest-runner'],
    tests_require=['pytest', 'pytest-cov'],
    
    packages=['momba'],
    
    classifiers=[
        'Development Status :: 1 - Planning'
    ]
)
