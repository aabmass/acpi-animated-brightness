import os
from setuptools import setup, find_packages

def read(fname):
    with open(os.path.join(os.path.dirname(__file__), fname)) as f:
        return f.read()

setup(
    name='acpibacklight',
    version='0.1',
    packages=find_packages(),
    scripts=[],
    install_requires=['PyTweening==1.0.3'],

    entry_points={
        'console_scripts': [
            'acpi-ease-backlight = cli:backlight'      
        ],
    },

    author='Aaron Abbott',
    author_email='aabmass@gmail.com',
    description='Library and script for changing brightness on Linux via acpi. '
                'Allows for easing animations too!',

    keywords='acpi brightness backlight easing animation',
    long_description=read('README.rst'),
)
