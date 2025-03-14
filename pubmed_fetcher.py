import requests
import csv
from typing import List, Dict, Optional
from lxml import etree
import time

class PubMedFetcher:
    """A class to fetch and filter research papers from PubMed."""

    BASE_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    FETCH_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"

    def __init__(self, query: str, debug: bool = False):
        self.query = query
        self.debug = debug

    def fetch_papers(self) -> List[Dict]:
        """Fetch 5 papers from PubMed based on the query."""
        search_params = {
            "db": "pubmed",
            "term": self.query,
            "retmode": "json",
            "retmax": 10,  # Fetch 5 papers instead of 1
        }
        if self.debug:
            print(f"Fetching 10 papers for query: {self.query}")

        # Retry logic for API requests
        max_retries = 3
        for attempt in range(max_retries):
            try:
                response = requests.get(self.BASE_URL, params=search_params, timeout=60)
                response.raise_for_status()  # Raise an error for bad status codes

                # Parse JSON response
                data = response.json()
                paper_ids = data.get("esearchresult", {}).get("idlist", [])
                break  # Exit the retry loop if the request succeeds
            except (requests.exceptions.RequestException, ValueError) as e:
                #if self.debug:
                  #  print(f"Attempt {attempt + 1} failed: {e}")
                if attempt == max_retries - 1:
                    if self.debug:
                        print("Max retries reached. Failed to fetch papers.")
                    return []
                time.sleep(5)  # Wait 5 seconds before retrying

        if self.debug:
            print(f"Found {len(paper_ids)} papers.")

        papers = []
        if paper_ids:  # Process the first 5 papers
            for idx, paper_id in enumerate(paper_ids[:10]):  # Process up to 5 papers
                if self.debug:
                    print(f"Processing paper {idx + 1}/{len(paper_ids)}...")
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
        # Retry logic for API requests
        max_retries = 3
        for attempt in range(max_retries):
            try:
                response = requests.get(self.FETCH_URL, params=fetch_params, timeout=60)
                response.raise_for_status()  # Raise an error for bad status codes

                break  # Exit the retry loop if the request succeeds
            except requests.exceptions.RequestException as e:
                if self.debug:
                    print(f"Attempt {attempt + 1} failed: {e}")
                if attempt == max_retries - 1:
                    if self.debug:
                        print("Max retries reached. Failed to fetch paper details.")
                    return None
                time.sleep(5)  # Wait 5 seconds before retrying

        # Parse XML response using lxml
        paper_xml = response.text
        title = self._extract_from_xml(paper_xml, "ArticleTitle")
        pub_date = self._extract_pub_date(paper_xml)  # Extract publication date
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
        """Extract text from an XML tag using lxml."""
        try:
            root = etree.fromstring(xml.encode("utf-8"))
            element = root.find(f".//{tag}")
            if element is not None and element.text is not None:
                return element.text.strip()
        except Exception as e:
            if self.debug:
                print(f"Error extracting {tag} from XML: {e}")
        return ""

    def _extract_pub_date(self, xml: str) -> str:
        """Extract publication date from XML."""
        try:
            root = etree.fromstring(xml.encode("utf-8"))
            pub_date = root.find(".//PubDate")
            if pub_date is not None:
                year = pub_date.findtext("Year", "").strip()
                month = pub_date.findtext("Month", "").strip()
                day = pub_date.findtext("Day", "").strip()
                return f"{year}-{month}-{day}" if year and month and day else ""
        except Exception as e:
            if self.debug:
                print(f"Error extracting publication date from XML: {e}")
        return ""

    def _extract_authors(self, xml: str) -> List[Dict]:
        """Extract authors and their affiliations from XML using lxml."""
        authors = []
        try:
            root = etree.fromstring(xml.encode("utf-8"))
            for author in root.xpath("//Author"):
                last_name = author.findtext("LastName", "").strip()
                fore_name = author.findtext("ForeName", "").strip()
                affiliation = author.findtext("Affiliation", "").strip()
                if last_name:  # Only include authors with a last name
                    authors.append({
                        "name": f"{fore_name} {last_name}",
                        "affiliation": affiliation
                    })
        except Exception as e:
            if self.debug:
                print(f"Error parsing XML for authors: {e}")
        return authors

    def _filter_authors(self, authors: List[Dict]) -> (List[str], List[str]):
        """Filter authors with pharmaceutical or biotech affiliations."""
        company_authors = []
        company_affiliations = []
        keywords = ["pharma", "biotech", "pharmaceutical", "biotechnology"]  # Keywords to filter affiliations

        for author in authors:
            affiliation = author.get("affiliation", "").lower()
            if any(keyword in affiliation for keyword in keywords):
                company_authors.append(author["name"])
                company_affiliations.append(author["affiliation"])

        # If no company authors found, return all authors regardless of affiliation
        if not company_authors:
            company_authors = [author["name"] for author in authors]
            company_affiliations = [author["affiliation"] for author in authors]

        #if self.debug:
         #   print(f"Filtered authors: {company_authors}")
          #  print(f"Filtered affiliations: {company_affiliations}")

        return company_authors, company_affiliations

    def save_to_csv(self, papers: List[Dict], filename: str = None):
        """Save the results to a CSV file or print to console."""
        if not papers:
            print("No papers found.")
            return

        #if self.debug:
         #   print(f"Papers to save: {papers}")  # Debug print

        if filename:
            try:
                with open(filename, "w", newline="", encoding="utf-8") as csvfile:
                    writer = csv.DictWriter(csvfile, fieldnames=papers[0].keys())
                    writer.writeheader()
                    writer.writerows(papers)
                if self.debug:
                    print(f"Results saved to {filename}.")
            except Exception as e:
                print(f"Error saving to CSV: {e}")
        else:
            for paper in papers:
                print(paper)
