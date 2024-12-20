from setuptools import setup, find_packages

setup(
    name="splicer-cli",
    version="1.0.3",
    author="AJ Rasmussen",
    author_email="ajrpeggio@gmail.com",
    description="A utility to copy audio files from a Splice folder to a final directory's staging directory.",
    long_description=open("README.md").read(),  # Create a README.md file for detailed project info
    long_description_content_type="text/markdown",
    url="https://github.com/ajrpeggio/splicer",  # Replace with the repository URL
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[],  # Specify any dependencies your script needs
    entry_points={
        "console_scripts": [
            "splicer = splicer.cli:main",
        ],
    },
    package_data={
        "": ["*.md"],  # Include additional files such as README.md
    },
    include_package_data=True,
)
