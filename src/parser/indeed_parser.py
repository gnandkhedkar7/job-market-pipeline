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