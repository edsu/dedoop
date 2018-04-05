from setuptools import setup

setup(
    name = 'dedoop',
    version = '0.0.3',
    author = 'Ed Summers',
    author_email = 'ehs@pobox.com',
    url = 'https://github.com/edsu/dedoop',
    py_modules = ['dedoop',],
    description = 'dedupe a directory of files and subdirectories',
    install_requires = [],
    setup_requires=['pytest-runner'],
    tests_require = ['pytest'],
    entry_points = {'console_scripts': ['dedoop = dedoop:main']},
)
