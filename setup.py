from setuptools import setup, find_packages

with open("README.md", "r") as desc:
    long_desc = desc.read()

setup(
    name='iad.py',
    version='1.0.0',
    lisence='MIT',
    description='A Python Wrapper for the im-a-dev.xyz uploader.',
    long_description=long_desc,
    long_description_content_type='text/markdown',
    url='https://im-a-dev.xyz/',
    author='fxcilities',
    packages=find_packages(),
    install_requires=['asyncio',
                      'aiohttp',                   
                      ],                    
)                      
