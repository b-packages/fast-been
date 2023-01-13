from setuptools import setup, find_packages

__version__ = '1.00'
__name__ = 'fast_been'
__author__ = 'hydra'
__author_email__ = 'navidsoleymani@ymail.com'
__license__ = 'BEENSI'
__url__ = 'https://github.com/b-packages/fast-been.git'
__keywords__ = 'fast_been fastapi',

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
    install_requires=[],
    # install_requires=[
    #     'fastapi',
    #     'pydantic',
    #     'SQLAlchemy',
    #     'python-jose',
    #     'passlib',
    # ],
)
