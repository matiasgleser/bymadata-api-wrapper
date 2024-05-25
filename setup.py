from setuptools import setup, find_packages

# Read the requirements from the requirements.txt file
with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name="bymadata_api_wrapper",
    version="0.1.0",
    packages=find_packages(include=["bymadata_api_wrapper", "bymadata_api_wrapper.*"]),
    install_requires=requirements,
    author="Matias Gleser",
    author_email="mgleser@gdelplata.com",
    description="Unofficial BYMADATA API wrapper",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/matiasgleser/bymadata-api-wrapper",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
