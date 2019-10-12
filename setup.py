import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Django-ObjectiveChartJS",
    version="0.0.5",
    author="Iridium IO",
    author_email="iridium.io@outlook.com",
    description="A clean, class-based implementation of Chart.JS",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/IridiumIO/Django-Objective-Chart.JS",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Framework :: Django",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires='>=3.0',
)
