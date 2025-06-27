from setuptools import setup, find_packages
import os

# Read the README file
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Read requirements
with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="cleannet-shield",
    version="2.0.0",
    author="kWan",
    description="A comprehensive adult content blocker and recovery tool for Windows",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kWan/cleannet-shield",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Internet :: WWW/HTTP :: Browsers",
        "Topic :: System :: Networking :: Firewalls",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: Microsoft :: Windows",
        "Environment :: Win32 (MS Windows)",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=6.0",
            "black>=21.0",
            "flake8>=3.8",
            "mypy>=0.812",
        ],
    },
    entry_points={
        "console_scripts": [
            "cleannet-shield=main:main",
            "cleannet-launcher=launcher:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.json", "*.txt", "*.md", "*.ps1", "*.bat"],
        "config": ["*.json"],
        "scripts": ["*.bat", "*.ps1", "*.py"],
        "docs": ["*.md"],
    },
    data_files=[
        ("", ["README.md", "LICENSE", "requirements.txt"]),
        ("scripts", ["scripts/start.bat", "scripts/setup.bat"]),
    ],
    project_urls={
        "Bug Reports": "https://github.com/kWan/cleannet-shield/issues",
        "Source": "https://github.com/kWan/cleannet-shield",
        "Documentation": "https://github.com/kWan/cleannet-shield/tree/main/docs",
    },
    keywords=[
        "content-blocker",
        "parental-control",
        "recovery-tool",
        "addiction-recovery",
        "windows-security",
        "dns-filtering",
        "hosts-blocker",
        "accountability",
        "streak-tracking",
        "journaling",
    ],
    platforms=["Windows"],
    license="MIT",
    zip_safe=False,
)
