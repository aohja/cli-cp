'''Installation scrip run by pip'''
from setuptools import setup, find_packages

setup(
    name='cp_cli',
    version='0.1',
    packages=find_packages(),
    python_requires='>=3.9',
    entry_points={
        'console_scripts': [
            'cph = cp_cli:main',
        ],
    },
)
