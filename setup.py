import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

with open('requirements.txt') as f:
    required = f.read().splitlines()

setuptools.setup(
    name="luthor-for-lex",
    version='0.0.13',
    author="Troy Larson",
    author_email="troylar@gmail.com",
    description="Easy Lex bot manager",
    long_description=long_description,
    install_requires=required,
    url="https://github.com/troylar/luthor-for-lex",
    packages=["speaker", "lex", "cli", "lex.fluent"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        'console_scripts': ['luthor=cli.main:cli'],
    }
)
