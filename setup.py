import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="zzo-bibtex-importer", # Replace with your own username
    version="0.0.1",
    author="zzossig",
    author_email="zzossig@gmail.com",
    description="bibtex importer for hugo zzo theme",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/zzossig/zzo-bibtex-importer",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: WTFPL License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)