from setuptools import setup

setup(
    name='installer',
    version='1.0',
    py_modules=['main'],
    entry_points={
        'console_scripts': [
            'installer = main:main',
        ],
    },
)
