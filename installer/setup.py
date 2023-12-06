from setuptools import setup

setup(
    name='my_package',
    version='1.0',
    py_modules=['main'],
    entry_points={
        'console_scripts': [
            'my_package = main:main',
        ],
    },
)
