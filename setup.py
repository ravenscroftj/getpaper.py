from setuptools import setup, find_packages

setup(
    name = "getpaper-py",
    version = 0.1,
    include_package_data = True,
    author="James Ravenscroft",
    author_email = "ravenscroft@papro.org.uk",
    description = "A janky script for downloading scientific papers from open access providers",
    url="http://brainsteam.co.uk/",

    install_requires=["requests==2.9.1"],
    py_modules=['getpaper']
)
