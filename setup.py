from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="nsepy",
    version="0.1.0",
    author="Anil Sardiwal",
    author_email="theonlyanil@gmail.com",
    description="A Python library for accessing data from the National Stock Exchange (NSE) of India.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/theonlyanil/nsepy",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        "pandas==2.2.3",
        "stealthkit==0.1.3",
    ],
)