import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pydero-jonlindg",
    version="1.0.1",
    author="Jonathan Lindgren",
    author_email="ejonathanlindgren@gmail.com",
    description="Python wrapper for interacting with the DERO blockdag",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jonlindg/pydero",
    packages=setuptools.find_packages(),
    install_requires=[
              'requests',
          ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
