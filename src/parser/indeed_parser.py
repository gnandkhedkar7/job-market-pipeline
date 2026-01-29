from bs4 import BeautifulSoup


def extract_title(raw_html: str) -> str | None:
    if not raw_html:
        return None

    soup = BeautifulSoup(raw_html, "html.parser")

    # Indeed-specific selector
    title_tag = (
    soup.select_one("h1[data-testid]")
    or soup.select_one("h1")
)

    if title_tag:
        return title_tag.get_text(strip=True)

    return None
