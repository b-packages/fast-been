from setuptools import setup, find_packages
from fast_been import __version__

setup(
    name='fast_been',
    version=__version__,
    license='BEENSI',
    author='nvd',
    author_email='navidsoleymani@ymail.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://github.com/b-packages/fast-been.git',
    keywords='fast_been fastapi',
    install_requires=[
        'fastapi',
        'pydantic',
        'SQLAlchemy',
        'python-jose',
        'passlib',
    ],
)
