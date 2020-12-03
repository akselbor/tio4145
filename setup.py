import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setuptools.setup(
    name="tio4145",  # Replace with your own username
    version="0.0.1",
    author="Aksel Borgen",
    author_email="akselborgen@outlook.com",
    description="Helper library used for the TIØ4145 exam",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/akselbor/tio4145",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=requirements,
    python_requires='>=3.6',
)
