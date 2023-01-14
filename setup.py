from setuptools import setup, find_packages

setup(
    name='fast_been',
    version='1.01',
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
