from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = 'Create crosswalk file for Swiss municipalities'
LONG_DESCRIPTION = 'Create a crosswalk file for Swiss municipalities between two points in time beetween '

# Setting up
setup(
    # the name must match the folder name 'verysimplemodule'
    name="create_crosswalk",
    version=VERSION,
    author="Vanessa Sticher",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[
        "pandas>=1.1.5",
        "numpy>=1.20.3",
        "pandas=>1.1.5",
        "requests>=2.25.1",
    ],
    keywords=['Swiss municipalities', 'crosswalk'],
    classifiers=[
        "Intended Audience :: Science/Research",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
