import os
import sys
import pathlib
from setuptools import setup, find_packages


def parse_requirements(filename):
    """ load requirements from a pip requirements file. (replacing from pip.req import parse_requirements)"""
    lineiter = (line.strip() for line in open(filename))
    return [line for line in lineiter if line and not line.startswith("#")]


reqs = parse_requirements('requirements.txt')
if sys.platform == "win32":
    reqs.append('pywin32')
    reqs.append('pyautogui')


here = pathlib.Path(__file__).parent.resolve()

# Get the long description from the README file
long_description = (here / 'README.md').read_text(encoding='utf-8')

setup(
    name='airobots',
    version='1.0.0',
    author='贝克街的捉虫师',
    author_email='forpeng@foxmail.com',
    description='UI Test Automation Framework for Games and Apps on Android/iOS/Windows/Linux/Web',
    long_description=long_description,  # Optional
    long_description_content_type='text/markdown',  # Optional (see note above)
    url='https://github.com/BSTester/Airobot',
    license='Apache License 2.0',
    keywords=['automation', 'automated-test', 'game', 'android', 'ios', 'windows', 'linux'],
    package_dir={'': 'src'},  # Optional
    packages=find_packages(where='src'),
    install_requires=reqs,
    entry_points="""
    [console_scripts]
    airobot = airobot.__main__:main
    """,
    classifiers=[
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)
