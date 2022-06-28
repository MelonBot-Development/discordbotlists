from setuptools import setup

from botlists import __title__, __author__, __version__

with open("requirements.txt", "r") as f:
    requirements = f.readlines()
    
with open("README.md", "r") as f:
    readme = f.read()
    
setup(
    name=__title__,
    author=__author__,
    url="https://github.com/MelonBot-Development/discordbotlists",
    version=__version__,
    packages=["botlists"],
    python_requires=[">=3.5"],
    include_package_data=True,
    install_requires=requirements,
    description="An api wrapper for botblock.org.",
    long_description=readme,
    long_description_content_type="text/markdown",
    keywords="botblock",
    classifiers=(
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.x.x",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
    ),
    project_urls={
        "Source": "https://github.com/MelonBot-Development/discordbotlists",
    },
)
