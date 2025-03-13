import requests
import csv
from typing import List, Dict, Optional

class PubMedFetcher:
    """A class to fetch and filter research papers from PubMed."""

    BASE_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    FETCH_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"

    def __init__(self, query: str, debug: bool = False):
        self.query = query
        self.debug = debug

    def fetch_papers(self) -> List[Dict]:
        """Fetch papers from PubMed based on the query."""
        search_params = {
            "db": "pubmed",
            "term": self.query,
            "retmode": "json",
            "retmax": 1000,  # Adjust as needed
        }
        if self.debug:
            print(f"Fetching papers for query: {self.query}")

        response = requests.get(self.BASE_URL, params=search_params)
        if response.status_code != 200:
            raise Exception(f"Failed to fetch papers: {response.status_code}")

        paper_ids = response.json().get("esearchresult", {}).get("idlist", [])
        if self.debug:
            print(f"Found {len(paper_ids)} papers.")

        papers = []
        for paper_id in paper_ids:
            paper_details = self._fetch_paper_details(paper_id)
            if paper_details:
                papers.append(paper_details)

        return papers

    def _fetch_paper_details(self, paper_id: str) -> Optional[Dict]:
        """Fetch details for a single paper."""
        fetch_params = {
            "db": "pubmed",
            "id": paper_id,
            "retmode": "xml",
        }
        response = requests.get(self.FETCH_URL, params=fetch_params)
        if response.status_code != 200:
            return None

        # Parse XML response (simplified for brevity)
        paper_xml = response.text
        title = self._extract_from_xml(paper_xml, "ArticleTitle")
        pub_date = self._extract_from_xml(paper_xml, "PubDate")
        authors = self._extract_authors(paper_xml)
        email = self._extract_from_xml(paper_xml, "Email")

        # Filter authors with pharmaceutical or biotech affiliations
        company_authors, company_affiliations = self._filter_authors(authors)

        if company_authors:
            return {
                "PubmedID": paper_id,
                "Title": title,
                "Publication Date": pub_date,
                "Non-academic Author(s)": ", ".join(company_authors),
                "Company Affiliation(s)": ", ".join(company_affiliations),
                "Corresponding Author Email": email,
            }
        return None

    def _extract_from_xml(self, xml: str, tag: str) -> str:
        """Extract text from an XML tag (simplified)."""
        start_tag = f"<{tag}>"
        end_tag = f"</{tag}>"
        start = xml.find(start_tag)
        end = xml.find(end_tag)
        if start != -1 and end != -1:
            return xml[start + len(start_tag) : end].strip()
        return ""

    def _extract_authors(self, xml: str) -> List[Dict]:
        """Extract authors and their affiliations from XML."""
        # Simplified extraction; use an XML parser for robust parsing.
        authors = []
        author_blocks = xml.split("<Author>")
        for block in author_blocks[1:]:
            name = self._extract_from_xml(block, "LastName")
            affiliation = self._extract_from_xml(block, "Affiliation")
            if name and affiliation:
                authors.append({"name": name, "affiliation": affiliation})
        return authors

    def _filter_authors(self, authors: List[Dict]) -> (List[str], List[str]):
        """Filter authors with pharmaceutical or biotech affiliations."""
        company_authors = []
        company_affiliations = []
        for author in authors:
            affiliation = author.get("affiliation", "").lower()
            if self.debug:
                print(f"Author: {author['name']}, Affiliation: {affiliation}")  # Debug print
            # Check if the affiliation contains any company-related keywords
            if (
                "pharma" in affiliation
                or "biotech" in affiliation
                or "inc" in affiliation
                or "corp" in affiliation
                or "ltd" in affiliation
                or "company" in affiliation
                or "research" in affiliation  # Add more keywords if needed
                or "drug" in affiliation
                or "medicine" in affiliation
                or "healthcare" in affiliation
                or "clinical" in affiliation
                or "therapy" in affiliation
                or "pharmaceutical" in affiliation  # Added
                or "biotechnology" in affiliation  # Added
                or "medical" in affiliation  # Added
                or "center" in affiliation  # Added
                or "institute" in affiliation  # Added
                or "foundation" in affiliation  # Added
                or "hospital" in affiliation  # Added
                or "clinic" in affiliation  # Added
                or "group" in affiliation  # Added
                or "organization" in affiliation  # Added
            ):
                company_authors.append(author["name"])
                company_affiliations.append(author["affiliation"])
        return company_authors, company_affiliations

    def save_to_csv(self, papers: List[Dict], filename: str = None):
        """Save the results to a CSV file or print to console."""
        if not papers:
            print("No papers found.")
            return

        if filename:
            with open(filename, "w", newline="", encoding="utf-8") as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=papers[0].keys())
                writer.writeheader()
                writer.writerows(papers)
            if self.debug:
                print(f"Results saved to {filename}.")
        else:
            for paper in papers:
                print(paper)