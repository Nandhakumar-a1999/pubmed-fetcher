import argparse
from pubmed_fetcher import PubMedFetcher

def main():
    parser = argparse.ArgumentParser(description="Fetch research papers from PubMed.")
    parser.add_argument("query", type=str, help="PubMed search query.")
    parser.add_argument("-d", "--debug", action="store_true", help="Enable debug mode.")
    parser.add_argument("-f", "--file", type=str, help="Save results to a CSV file.")

    args = parser.parse_args()

    fetcher = PubMedFetcher(query=args.query, debug=args.debug)
    papers = fetcher.fetch_papers()
    fetcher.save_to_csv(papers, filename=args.file)

if __name__ == "__main__":
    main()