import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="DYESOPT_pkg",
    version="0.1",
    author="Example Author",
    author_email="author@example.com",
    description="DYNAMIC ENERGY SYSTEM OPTIMIZER",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/XXXXXX",
    packages=setuptools.find_packages(),
    REQUIRES_PYTHON = '=3.6',
    install_requires=['xlrd','pandas','scipy','pvlib','iapws','pywinauto'],
    classifiers=(
        "Programming Language :: Python :: 3.6",
        "License :: XXXXXXX :: XXXXXX",
        "Operating System :: Windows dependent",
    ),
)
