from setuptools import setup

setup(
    name = 'dedoop',
    version = '0.0.1',
    author = 'Ed Summers',
    author_email = 'ehs@pobox.com',
    url = 'https://github.com/edsu/deduper',
    py_modules = ['deduper',],
    description = 'dedupe a directory of files and subdirectories',
    install_requires = [],
    setup_requires=['pytest-runner'],
    tests_require = ['pytest'],
    entry_points = {'console_scripts': ['deduper = deduper:main']},
)
