from setuptools import setup, find_packages

# Read requirements from requirements.txt
with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="agentsync",  # Lowercase package name
    version="0.0.2",
    packages=find_packages(),  # Automatically finds submodules
    install_requires=requirements,
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "agentsync=agentsync.config:main",  # Adjust if needed
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.11",
)
