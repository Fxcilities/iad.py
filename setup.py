from setuptools import setup, find_packages

setup(
    name='iad.py',
    version='1.0.3',
    lisence='MIT',
    description='A Python Wrapper for the im-a-dev.xyz uploader.',
    long_description=open("README.md", "r").read(),
    long_description_content_type='text/markdown',
    url='https://im-a-dev.xyz/',
    author='fxcilities',
    packages=find_packages(),
    install_requires=['aiohttp'],                    
)