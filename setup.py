import setuptools

with open("README.md") as file:
    descr = file.read()

setuptools.setup(
    name="cxx",
    version="0.0.1",
    author="Rubbie Kelvin Voltsman",
    author_email="rubbiekelvinvoltsman@gmail.com",
    description="simple crypting library ;)",
    long_description=descr,
    long_description_content_type="text/markdown",
    url="https://rubbiekelvin@bitbucket.org/rubbiekelvin/cxx",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.0'
)
