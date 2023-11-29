from setuptools import setup

setup(
    name='togglesmell_detector_installer',
    version='1.0',
    py_modules=['nested-toggle-extraction'],
    entry_points={
        'console_scripts': [
            'togglesmell_detector_installer = nested-toggle-extraction:nested_toggle',
        ],
    },
)
