from setuptools import setup, find_packages

setup(
    name='modules_feeds',
    version='1.0.0',
    description='This is a working setup.py',
    url='',
    author='Carmen Fuentes and Raul Fernández',
    author_email='cfuentes@cheil.com',
    packages=find_packages(),
    install_requires=[
        'requests','pandas','pyyaml','bs4','sqlalchemy'
    ],
    zip_safe=False
)