from setuptools import setup, find_packages

setup(
    name='beensi_framework',
    version='0.01',
    license='BEENSI',
    author='nvd',
    author_email='navidsoleymani@ymail.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    # url='',
    # keywords='',
    install_requires=[
    ],
)
