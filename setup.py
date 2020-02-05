import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

install_requires = ['bibtexparser==1.1.0']

setuptools.setup(
    name="zzo-bibtex-parser",
    version="1.0.5",
    license="WTFPL",
    author="zzossig",
    author_email="zzossig@gmail.com",
    description="bibtex importer for hugo zzo theme",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/zzossig/zzo-bibtex-parser",
    packages=setuptools.find_packages(),
    entry_points ={
        'console_scripts': [ 
            'zzo = zzo.parser:main'
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=install_requires,
)