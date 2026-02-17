#!/usr/bin/env python3
"""Setup script for Sinyfy package."""

import os
from setuptools import setup, find_packages

# Read the contents of README.md
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="Sinyfy",
    version="1.0.0",
    author="thetemirbolatov",
    author_email="mirajestory@gmail.com",
    description="Sinyfy - Static Site Visual Cloner (Без Selenium)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/thetemirbolatov-official/Sinyfy",
    project_urls={
        "Bug Tracker": "https://github.com/thetemirbolatov-official/Sinyfy/issues",
        "Documentation": "https://github.com/thetemirbolatov-official/Sinyfy#readme",
        "Source Code": "https://github.com/thetemirbolatov-official/Sinyfy",
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    py_modules=["Sinyfy"],  # Указываем модуль в корне
    python_requires=">=3.7",
    install_requires=[
        "requests>=2.25.0",
        "beautifulsoup4>=4.9.0",
        "Pillow>=8.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov>=2.0",
            "black>=21.0",
            "flake8>=3.9",
            "mypy>=0.900",
            "build>=0.7.0",
            "twine>=3.4.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "Sinyfy=Sinyfy:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)