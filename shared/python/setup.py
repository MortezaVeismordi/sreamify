from setuptools import setup, find_packages

setup(
    name='streamify-common',
    version='0.1.0',
    description='Shared library for Streamify microservices',
    packages=find_packages(),
    install_requires=[
        'Django>=5.0.0',
        'djangorestframework>=3.14.0',
        'PyJWT>=2.8.0',
    ],
)
