from bs4 import BeautifulSoup

def extract_page_title(raw_html: str) -> str | None:
    if not raw_html:
        return None

    soup = BeautifulSoup(raw_html, "html.parser")

    if soup.title:
        return soup.title.get_text(strip=True)

    return None

def extract_job_titles(raw_html: str) -> list[str]:
    if not raw_html:
        return []
    
    soup = BeautifulSoup(raw_html, "html.parser")
    
    titles = []
    
    for span in soup.find_all("span", id=lambda x: x and x.startswith("jobTitle-")):
        text = span.get_text(strip=True)
        if text:
            titles.append(text)
            
    return titles

def extract_job_cards(raw_html: str) -> list[dict]:
    """
    Extract job cards from an Indeed search results page.
    Returns a list of dicts with job_id and title.
    """
    if not raw_html:
        return []

    soup = BeautifulSoup(raw_html, "html.parser")
    jobs = []

    for a in soup.find_all("a", attrs={"data-jk": True}):
        job_id = a.get("data-jk")

        title_span = a.find("span", id=lambda x: x and x.startswith("jobTitle-"))
        title = title_span.get_text(strip=True) if title_span else None
        
        job_li = a.find_parent("li")
        
        company_span =  (
            job_li.find("span", attrs={"data-testid": "company-name"})
            if job_li else None
        )
        
        company = company_span.get_text(strip=True) if company_span else None
        
        location_div = job_li.find("div", attrs={"data-testid": "text-location"})
        location = location_div.get_text(strip=True) if location_div else None
        
        if job_id and title:
            jobs.append(
                {
                    "job_id": job_id,
                    "title": title,
                    "company": company,
                    "location": location
                }
            )

    return jobs
