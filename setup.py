#!/usr/bin/env python3

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="loyaltylt-sdk",
    version="1.0.3",
    author="Loyalty.lt",
    author_email="developers@loyalty.lt",
    description="Official Python SDK for Loyalty.lt Shop API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Loyalty-lt/sdk-python",
    project_urls={
        "Bug Tracker": "https://github.com/Loyalty-lt/sdk-python/issues",
        "Documentation": "https://docs.loyalty.lt/sdk/python",
        "Homepage": "https://loyalty.lt",
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[
        "requests>=2.28.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
        ],
    },
    keywords=[
        "loyalty",
        "points",
        "rewards",
        "sdk",
        "api",
        "pos",
        "qr-login",
    ],
)
