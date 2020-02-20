import os

import setuptools


def get_version():
    package_init = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'graphql_utilities', '__init__.py')
    with open(package_init) as f:
        for line in f:
            if line.startswith('__version__ ='):
                return line.split('=')[1].strip().strip('"\'')


def get_long_description():
    with open("README.md", "r") as fh:
        return fh.read()


setuptools.setup(
    name="graphql-utilities",
    version=get_version(),
    author="Melvin Koh",
    author_email="melvinkcx@gmail.com",
    description="Collection of utilities, middleware, decorators for graphql-core>=3.0",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    url="https://github.com/melvinkcx/graphql-utilities",
    packages=setuptools.find_packages(exclude=["tests.*"]),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.5',
        'Topic :: Software Development :: Libraries'
    ],
    install_requires=['graphql-core>=3.0'],
    python_requires=">=3.6,<4",
    extras_require={
        'dev': [
            'pytest>=5.3.4,<6',
            'flake8>=3.7.9,<4',
            'pytest-describe>=0.12,<1',
            'django>=1.11,<3',
        ]
    }
)
