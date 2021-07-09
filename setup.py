import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name='Tasc_6 Report of Monaco 2018 Racing',
    version='0.0.1',
    author="Anton Viazovic",
    author_email="loukik56@mail.ru",
    description="Create report from raw data F1",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://git.foxminded.com.ua/Anton1/report-of-monaco-2018-racing.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.7",
    ],
    python_requires='>=3.7',
)

