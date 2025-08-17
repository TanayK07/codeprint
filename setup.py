from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="codeprintio",
    version="1.0.0",
    author="Tanayk07",
    description="AI-ready code snapshots for any project",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Tanayk07/codeprint",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=[
        "colorama>=0.4.4",
        "pyperclip>=1.8.2",
    ],
    entry_points={
        "console_scripts": [
            "codeprint=codeprint.cli:main",
            "codep=codeprint.cli:main",
        ],
    },
)
