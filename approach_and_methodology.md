# Approach and Methodology for Fetching Research Papers from PubMed

## Objective:
The goal of the program is to fetch research papers from PubMed based on a user-specified query. The program filters the papers to identify those with at least one author affiliated with a pharmaceutical or biotech company. It then returns the results in a CSV format with the required details.

## Steps in the Approach:

### 1. Fetching Paper Metadata:
- **PubMed API**: The PubMed API (eUtils) is used to search for papers based on the user-provided query. 
    - The `esearch` endpoint is used to retrieve paper IDs matching the search criteria.
    - After obtaining the paper IDs, the `efetch` endpoint is used to fetch detailed information about each paper, such as the title, authors, and publication date.

### 2. Parsing the XML Response:
- **XML Parsing**: PubMed returns paper metadata in XML format. The program uses the `lxml` library to parse the XML responses and extract the necessary information such as:
  - Paper’s title
  - Publication date
  - Authors
  - Affiliations
  - Corresponding author’s email

### 3. Filtering Non-academic Authors:
- **Author Affiliation Filtering**: For each paper, the affiliations of all authors are checked for keywords that are typically associated with pharmaceutical or biotech companies (such as "pharma", "biotech", "biotechnology").
  - Authors with such affiliations are considered non-academic and are filtered out for inclusion in the output.

### 4. Data Formatting:
- **Data Organization**: The relevant paper metadata is formatted as a dictionary with the following keys:
  - PubMed ID
  - Title
  - Publication Date
  - Non-academic Authors
  - Company Affiliations
  - Corresponding Author Email

### 5. Output Generation:
- **CSV Output**: The program either prints the output to the console or saves it to a CSV file, depending on the user's command-line input. The CSV will have the following columns:
  - PubMed ID
  - Title
  - Publication Date
  - Non-academic Authors
  - Company Affiliations
  - Corresponding Author Email

### 6. Command-Line Interface (CLI):
- The program provides a command-line interface that accepts:
  - A search query
  - An optional output filename for the CSV file
  - A debug flag.
  
  This makes the program flexible and easy to use for different queries and output preferences.

### 7. Error Handling:
- The program includes robust error handling to deal with:
  - API request failures (with retry logic)
  - Missing or incomplete data in the XML response
  - Incorrect or invalid user input.
  
  It prints meaningful debug messages in debug mode to help the user troubleshoot.

### 8. Code Modularity:
- The code is structured into modular components:
  - **PubMedFetcher Class**: Handles the API interaction, XML parsing, and data filtering.
  - **Command-Line Interface**: Manages user input, invokes the PubMedFetcher class, and handles output generation.

### 9. Dependencies:
The program uses the following libraries:
- `requests`: To make HTTP requests to the PubMed API.
- `lxml`: For XML parsing and extraction of metadata.
- `csv`: For generating the output CSV file.
- `Poetry`: For dependency management.

## Result

### CSV Output:
Upon executing the program, the following results are generated:

- **CSV Output**: The program generates a CSV file (or prints to the console if no file is specified) that contains information about research papers with at least one author affiliated with pharmaceutical or biotech companies. The CSV file will have the following columns:
  - PubMed ID: A unique identifier for the paper.
  - Title: The title of the paper.
  - Publication Date: The date the paper was published (in YYYY-MM-DD format).
  - Non-academic Author(s): The names of authors affiliated with pharmaceutical or biotech companies.
  - Company Affiliation(s): The names of pharmaceutical or biotech companies affiliated with the non-academic authors.
  - Corresponding Author Email: The email address of the corresponding author (if available).

#### Example CSV:
| PubMed ID | Title                                     | Publication Date | Non-academic Author(s) | Company Affiliation(s) | Corresponding Author Email |
|-----------|-------------------------------------------|------------------|------------------------|------------------------|----------------------------|
| 12345678  | Novel Approaches to Drug Development      | 2025-03-12       | Dr. John Doe           | BioPharma Inc.         | john.doe@biopharma.com     |
| 23456789  | Advances in Cancer Gene Therapy           | 2024-11-20       | Dr. Jane Smith         | Biotech Solutions      | jane.smith@biotech.com     |

### CLI Execution:

The user can specify a query to search PubMed (e.g., "cancer drug") and optionally provide an output file name. The program will fetch up to 5 papers matching the query and filter them based on authors' affiliations with pharmaceutical or biotech companies. The results will be printed to the console or saved to a CSV file as requested.

#### Example commands:
```bash
# Fetch papers related to "cancer drug" and save results to a CSV file
python get_papers_list.py --query "cancer drug" --file "cancer_drug_papers.csv"

# Fetch papers and print to console
python get_papers_list.py --query "gene therapy" --debug

# Display usage instructions
python get_papers_list.py --help
