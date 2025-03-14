# PubMed Fetcher

A Python tool to fetch and filter research papers from PubMed based on a search query. The tool allows you to retrieve paper details such as title, publication date, authors, affiliations, and corresponding author email. It also provides the option to save the results to a CSV file.

## Installation

To install the PubMed Fetcher, you can use Poetry, a dependency management tool for Python.

1. Install Poetry by following the instructions [here](https://python-poetry.org/docs/#installation).
2. Clone this repository.
3. Navigate to the project directory and run the following command to install the dependencies:

   ```bash
   poetry install
Usage
To fetch papers from PubMed, use the following command:

bash
Copy
poetry run get-papers-list "your search query" [-d] [-f filename.csv]
your search query: The search term to query PubMed.

-d or --debug: Enable debug mode for additional output.

-f or --file: Save the results to a CSV file with the specified filename.

Example
bash
Copy
poetry run get-papers-list "cancer treatment" -d -f results.csv
This command will fetch papers related to "cancer treatment", enable debug mode, and save the results to results.csv.

External Tools and Libraries
The PubMed Fetcher relies on the following external tools and libraries:

Requests: A simple and elegant HTTP library for Python, used to make API requests to PubMed.

Documentation

Version: ^2.26.0

lxml: A library for processing XML and HTML in Python, used to parse the XML response from PubMed.

Documentation

Version: Included in the standard library, but may require installation via pip install lxml.

Poetry: A dependency management and packaging tool for Python, used to manage project dependencies and build the package.

Documentation

Version: >=1.0.0

Contributing
Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

License
This project is licensed under the MIT License. See the LICENSE file for details.

Copy

This `README.md` file provides clear documentation on how to install, use, and contribute to the project, as well as the external tools and libraries used.