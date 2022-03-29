import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Task-6-Report-of-Monaco-2018-Racing",
    version="0.0.3",
    author="Anton Viazovik",
    author_email="Loukik56@mail.ru",
    description="This package processes driver statistics",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://git.foxminded.com.ua/Anton1/report-of-monaco-2018-racing",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(),
    python_requires='>=3.7',
)