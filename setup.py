import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

requirements = [
    "qiskit",
    "numpy",
    "pytest",
    "pytest-cov",
]

setuptools.setup(
    name="wigners_friend",
    version="1.0.0",
    description="Exploration of extended Wigners friend scenario",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Physics",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.11",
    install_requires=requirements,
    test_suite="tests",
)
