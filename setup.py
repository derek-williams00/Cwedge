import setuptools

long_description = "Python based build framework for C and C++."

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Cwedge-pkg",
    version="0.0.2",
    author="Derek Williams",
    author_email="derek@derekwilliams00.com",
    description="A Python based build framework for C and C++.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="http://github.com/derek-williams00/Cwedge",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    py_modules=['cwedge'],
    package_dir={'': 'src'},
    extras_require = {
        "dev": [
            "pytest>=3.7",
            "twine>=3.0",
        ],
    },
)


