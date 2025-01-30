from setuptools import setup, find_packages

setup(
    name='pycses',
    version='0.1',
    author='unDefFtr',
    author_email='undefftr@undefined.ac.cn',
    description='CSES access framework for Python',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/CSES-org/pycses',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
