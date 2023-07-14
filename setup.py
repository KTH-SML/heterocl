import setuptools

def parse_requirements(filename):
    """Load requirements from a pip requirements file."""
    lineiter = (line.strip() for line in open(filename))
    return [line for line in lineiter if line and not line.startswith("#")]

def setup():
    with open("README.md", encoding="utf-8") as fp:
        long_description = fp.read()

    setuptools.setup(
        name="heterocl",
        description="HeteroCL: A Multi-Paradigm Programming Infrastructure for Software-Defined Reconfigurable Computing",
        version="0.5",
        author="HeteroCL",
        long_description=long_description,
        long_description_content_type="text/markdown",
        install_requires=parse_requirements("requirements.txt") + ["hcl_mlir"],
        packages=setuptools.find_packages(),
        url="https://github.com/cornell-zhang/heterocl",
        python_requires=">=3.7",
        classifiers=[
            "Programming Language :: Python :: 3.7",
            "Programming Language :: Python :: 3.8",
            "Programming Language :: Python :: 3.9",
            "Programming Language :: Python :: 3.10",
            "Topic :: Scientific/Engineering",
            "Topic :: System :: Hardware",
            "Operating System :: OS Independent",
        ],
        zip_safe=True,
    )

if __name__ == "__main__":
    setup()
