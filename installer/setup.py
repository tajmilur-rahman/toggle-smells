from setuptools import setup

setup(
    name='togglesmell_detector_installer',
    version='1.0',
    py_modules=['main'],
    entry_points={
        'console_scripts': [
            'togglesmell_detector_installer = main:main',
        ],
    },
)