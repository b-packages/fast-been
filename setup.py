from setuptools import setup, find_packages

setup(
    name='beensi_framework',
    version='0.003',
    license='BEENSI',
    author='nvd',
    author_email='navidsoleymani@ymail.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://github.com/b-packages/beensi-framework.git',
    keywords='beensi_framework',
    install_requires=[
        'fastapi',
        'pydantic',
        'SQLAlchemy',
        'python-jose',
        'passlib',
    ],
)
