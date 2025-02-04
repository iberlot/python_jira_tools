""" Setup file for the Jira Data Library. """

from setuptools import setup, find_packages

setup(
    name="jira-data-library",
    version="0.1.0",
    description="A Python library to fetch data from Jira.",
    author="iBerlot",
    author_email="ivanberlot@gmail.com",
    packages=find_packages(),
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    install_requires=[
        "requests", "pytest", "responses", "fastapi", "typing"
    ],
    python_requires=">=3.7",
    url="https://github.com/iberlot/python_jira_tools",
)
