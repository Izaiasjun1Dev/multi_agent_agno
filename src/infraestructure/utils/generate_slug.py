import re


def generate_slug(text: str) -> str:
    # Implementação da geração de slug
    text = text.strip().lower()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s-]+", "-", text)
    return text
