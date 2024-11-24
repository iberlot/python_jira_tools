from setuptools import setup, find_packages

setup(
    name="jira-data-library",
    version="0.1.0",
    description="A Python library to fetch data from Jira.",
    author="Tu Nombre",
    author_email="tuemail@example.com",
    packages=find_packages(),
    install_requires=[
        "requests",
    ],
    python_requires=">=3.7",
)
