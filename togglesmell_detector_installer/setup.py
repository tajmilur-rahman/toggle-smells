from setuptools import setup, find_packages
setup(
    name='togglesmell_detector_installer',
    version='1.0',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'togglesmell_detector_installer = my_package.nested-toggle-extraction:nested_toggle',
        ],
    },
)
