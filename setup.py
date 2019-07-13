from setuptools import setup, find_packages

setup(
    name='listthedocs',
    version='1.0.0',
    description='List your docuemntation and versions',
    author='Rob Galanakis',
    author_email='rob.galanakis@gmail.com',
    url='https://github.com/rgalanakis/hostthedocs',
    packages=find_packages(),
    install_requires=[
        'Flask',
        'natsort',
    ],
)
