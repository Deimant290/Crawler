# Example Data Crawler

## Description

Example Data Crawler is a Python package designed for teaching the basics of web
crawling at CodeAcademy. This project is tailored for beginners and utilizes
Python 3.10, along with lxml and requests libraries, focusing on practical web
data extraction techniques.

## Installation

### Using a package manager

You can install the crawler as a package: Using `pip`:

```sh
pip install Crawler
```

Or using `poetry`:

```sh
poetry add Crawler
```

### Cloning the repository

You can also clone the repository and install the dependencies. Using `poetry`:

```sh
git clone https://github.com/Deimant290/pythonProject1/Crawler
cd Crawler
poetry install
```

## Usage

### As a module

```python

## Structure

The project is structured as follows:

- `Crawler/`: Main package directory.
  - `__init__.py`: Package initialization file.
  - `crawlers/`: Directory containing individual crawler scripts.
    - `__init__.py`: Initialization file for crawlers module.
    - `lrytas.py`: Crawler for the Lrytas website.
    - `definitions.py`: Definitions and utility functions.
  - `dl_image.py`: Script for downloading images.
  - `main.py`: Main script for the crawler package.
- `examples/`: Directory containing example scripts.
    - `all.py`: Example script for crawling all data.
    - `by_topic.py`: Example script for crawling by topic.
- `tests/`: Test scripts for the package.
  - `__init__.py`: Initialization file for tests.

## License

This project is licensed under the MIT license.