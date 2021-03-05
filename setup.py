# coding=utf8

import sys
import pathlib
from setuptools import setup, find_packages
from src.airobots import __version__

reqs = ["selenium", "airtest", "airtest_selenium", "pocoui","requests","pymysql","pymongo","pytest", "pm2case","pytest-selenium","pynput","pywinio","airhttprunner","airhttprunner[allure]","locust", "airhttprunner[locust]", "airhttprunner[upload]","allure-pytest", "pytest-repeat","paramiko","sshtunnel","AirobotLibrary"]
if sys.platform == "win32":
    reqs.append('pywin32')
    reqs.append('pyautogui')

here = pathlib.Path(__file__).parent.resolve()

# Get the long description from the README file
long_description = (here / 'README.md').read_text(encoding='utf-8')

setup(
    name='airobots',
    version=__version__,
    author='贝克街的捉虫师',
    author_email='forpeng@foxmail.com',
    description='UI Test Automation Framework for Games and Apps on Android/iOS/Windows/Linux/Web',
    long_description=long_description,  # Optional
    long_description_content_type='text/markdown',  # Optional (see note above)
    url='https://github.com/BSTester/Airobots',
    license='Apache License 2.0',
    keywords=['automation', 'automated-test', 'game', 'android', 'ios', 'windows', 'linux', 'web'],
    package_dir={'': 'src'},  # Optional
    packages=find_packages(where='src'),
    python_requires='>=3.5, <4',
    install_requires=reqs,
    entry_points="""
    [console_scripts]
    airobots = airobots.__main__:main
    """,
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 4 - Beta',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',

        # Pick your license as you wish
        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3 :: Only',
    ],
    project_urls={  # Optional
        # 'Bug Reports': 'https://github.com/pypa/sampleproject/issues',
        # 'Funding': 'https://donate.pypi.org',
        # 'Say Thanks!': 'http://saythanks.io/to/example',
        'Source': 'https://github.com/BSTester/Airobots',
    },
)
