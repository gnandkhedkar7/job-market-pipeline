from src.scraper.indeed_scraper import IndeedScraper

if __name__ == "__main__":
    scraper = IndeedScraper()
    scraper.scrape_search_page(
        query="data engineer",
        location="München"
    )
