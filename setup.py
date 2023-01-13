from setuptools import setup, find_packages
from fast_been import (
    __name__,
    __version__,
    __license__,
    __author__,
    __author_email__,
    __url__,
    __keywords__,
)

setup(
    name=__name__,
    version=__version__,
    license=__license__,
    author=__author__,
    author_email=__author_email__,
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url=__url__,
    keywords=__keywords__,
    install_requires=[
        'fastapi',
        'pydantic',
        'SQLAlchemy',
        'python-jose',
        'passlib',
    ],
)
