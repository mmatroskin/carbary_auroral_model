import pathlib
import setuptools

from carbary_model.__version__ import version


package_data = {"carbary_auroral_model": ["CHANGELOG.md", "LICENSE", "WWM.COF"]}
readme = pathlib.Path("README.md").read_text()
history = pathlib.Path("CHANGELOG.md").read_text()
description = f"{readme}\n\n## Changelog\n\n{history}"


setuptools.setup(
    name="carbary_auroral_model",
    version=version,
    author="Maksim Tulin",
    author_email="maks.u.tulin@gmail.com",
    description="Python implementation for J.F. Carbary auroral oval model (2005)",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/mmatroskin/carbary_auroral_model",
    project_urls={
        "Source": "https://github.com/mmatroskin/carbary_auroral_model",
        "Issues": "https://github.com/mmatroskin/carbary_auroral_model/issues",
    },
    packages=setuptools.find_packages(exclude=["tests"]),
    package_dir={"carbary_model": "./carbary_model"},
    package_data=package_data,
    include_package_data=True,
    license_files=["LICENSE"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Astronomy",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Programming Language :: Python :: 3.14",
        "Programming Language :: Python :: 3 :: Only",
    ],
    python_requires=">=3.10",
    install_requires=pathlib.Path("requirements/lib.txt").read_text().split(),
)
