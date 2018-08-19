import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="luthor-for-lex",
    version="0.0.1",
    author="Troy Larson",
    author_email="troylar@gmail.com",
    description="Easy Lex bot manager",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/troylar/luthor-for-lex",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points = {
        'console_scripts': ['luthor=cli:cli'],
    }
)
