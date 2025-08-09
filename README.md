<!-- omit from toc -->
# Project: Creating a Data Pipeline for HappyPaws

*A DataCamp project*

<!-- omit from toc -->
## Table of Contents
- [Overview](#overview)
- [Project Structure](#project-structure)
- [Data Source(s)](#data-sources)
- [Installation](#installation)
  - [Prerequisites](#prerequisites)
  - [Install dependencies](#install-dependencies)
- [Usage](#usage)
  - [Run a Jupyter Notebook](#run-a-jupyter-notebook)
- [Conclusions](#conclusions)
- [Technologies Used](#technologies-used)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Overview

This project performs cleaning and analysis using Python. This is done on three datasets supplied by a software developer: animal activity, animal health, and owner information. The goal is to merge the datasets into a single dataset usable by the development team and provide some basic insights from their data.

This is a portfolio project created to demonstrate my proficiency in data cleaning, analysis, and visualization, as well as creating functions to support that workflow using Python. It highlights my ability to work with real-world datasets, derive meaningful insights, and communicate results clearly through code and visualizations.

## Project Structure

```
└── 📁data-engineer-practical
    └── 📁assets
        ├── image.png
    └── 📁code
        └── 📁utilities
            ├── __init__.py
            ├── config.py
            ├── processes.py
        ├── notebook.ipynb
    └── 📁data
        ├── cleaned.csv
        ├── pet_activities.csv
        ├── pet_health.csv
        ├── users.csv
    └── 📁products
        └── 📁images
        ├── report.md
    ├── .gitignore
    ├── LICENSE
    ├── README.md
    └── requirements.txt
```

## Data Source(s)

- **File(s)**: [`pet_activities.csv`](./data/pet_activities.csv), [`pet_health.csv`](./data/pet_health.csv), [`users.csv`](./data/users.csv)
- **Source**: DataCamp
- **Description**: Data on pet activities, pet health, and pet owners.

## Installation

### Prerequisites

- Python 3.11+
- pip (Python package manager)

### Install dependencies

Create a virtual environment (optional but recommended):

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\\Scripts\\activate
pip install -r requirements.txt
```

Clone the repository and install required packages:

```bash
git clone https://github.com/kozmik-moore/pet-software-developer-pipeline.git
cd pet-software-developer-pipeline
pip install -r requirements.txt
```

## Usage

### Run a Jupyter Notebook

Start the Jupyter server:

```bash
jupyter notebook
```

Open and run notebooks from the [`/code`](/code/) directory to explore data and generate visualizations.

## Conclusions

See full visual report in [`/products/report.md`](/products/report.md).

## Technologies Used

- Python 3.11+
- [pandas](https://pandas.pydata.org/) – for data manipulation
- [seaborn](https://seaborn.pydata.org/) – for statistical data visualization
- [matplotlib](https://matplotlib.org/) – for low-level plotting
- [Jupyter Notebook](https://jupyter.org/) – for interactive analysis

## Contributing

Contributions are welcome. To contribute:

1. Fork the repository
2. Create a new branch (`git checkout -b feature-branch`)
3. Make your changes
4. Commit your changes (`git commit -m "Add feature"`)
5. Push to your branch (`git push origin feature-branch`)
6. Open a pull request

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

Kozmik Moore\
Email: koz.moore@gmail.com\
GitHub: [@kozmik-moore](https://github.com/kozmik-moore)\
LinkedIn: [@kozmik-moore](www.linkedin.com/in/kozmik-moore)
