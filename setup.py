from setuptools import setup

setup(
    name = 'dedoop',
    version = '0.0.3',
    author = 'Ed Summers',
    author_email = 'ehs@pobox.com',
    url = 'https://github.com/edsu/dedoop',
    py_modules = ['dedoop',],
    description = 'dedupe files and send them to the cloud',
    install_requires = ['apache-libcloud', 'python-dotenv'],
    setup_requires=['pytest-runner'],
    tests_require = ['pytest'],
    entry_points = {'console_scripts': ['dedoop = dedoop:main']},
)
