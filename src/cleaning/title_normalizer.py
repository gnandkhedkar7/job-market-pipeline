import re
import string

GENDER_PATTERNS = [
    r"\(m\/w\/d\)",
    r"\(w\/m\/d\)",
    r"\(m\/f\/d\)",
    r"\*",
]

def normalize_title(raw_title: str | None) -> tuple[str | None, str|None]:
    if not raw_title:
        return None, "missing_title"
    
    title = raw_title.lower()
    
    title = title.split("|")[0]
    
    for pattern in GENDER_PATTERNS:
        title = re.sub(pattern, "", title)
        
    title = re.sub(r"[\/\-_]", " ", title)
    
    title = title.translate(str.maketrans("","", string.punctuation))
    
    title = re.sub(r"\s+", " ", title).strip()
    
    if len(title) < 3:
        return None, "title_too_short"
    
    return title, None