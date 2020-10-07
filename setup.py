from pathlib import Path
from setuptools import setup

_classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Topic :: Software Development :: Libraries',
    'Topic :: Utilities',
]


def _version():
    with open('editor.py') as fp:
        line = next(i for i in fp if i.startswith('__version__'))
        return line.strip().split()[-1].strip("'")


REQUIREMENTS = Path('requirements.txt').read_text().splitlines()


if __name__ == '__main__':
    setup(
        name='editor',
        version=_version(),
        author='Tom Ritchford',
        author_email='tom@swirly.com',
        url='https://github.com/rec/editor',
        py_modules=['editor'],
        description='Open the default text editor',
        long_description=open('README.rst').read(),
        license='MIT',
        classifiers=_classifiers,
        keywords=['testing', 'modules'],
        install_requires=REQUIREMENTS,
    )
