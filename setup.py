#!/usr/bin/env python
# -*- coding: utf-8 -*-
try:
    from setuptools import setup
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup

setup(
    name='django-pages',
    version='0.1.0-alpha',
    description='A flexible pages application for django for future extending',
    author='Andrey Grygoryev',
    author_email='undeadgrandse@gmail.com',
    url='https://github.com/GrAndSE/django-pages',
    long_description=open('README', 'r').read(),
    packages=['pages'],
    package_data={
        'pages': [
            'templates/admin/includes/*',
            'templates/admin/page_change_form.html']
    },
    zip_safe=False,
    requires=[],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
)
