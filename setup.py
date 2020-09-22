from setuptools import setup

with open("README.md") as f:
    long_description = f.read()

setup(
    name = 'dedoop',
    version = '0.0.4',
    author = 'Ed Summers',
    author_email = 'ehs@pobox.com',
    url = 'https://github.com/edsu/dedoop',
    py_modules = ['dedoop',],
    description = 'dedupe files and send them to the cloud',
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires = ['apache-libcloud', 'click'],
    setup_requires=['pytest-runner'],
    tests_require = ['pytest', 'python-dotenv'],
    entry_points = {'console_scripts': ['dedoop = dedoop:main']},
)
