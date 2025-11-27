from typing import Any

import markdown
import structlog
from bs4 import BeautifulSoup

log = structlog.get_logger()

def parse_markdown(file_data: dict[str, Any]) -> dict[str, Any]:
    """
    Parses raw markdown content into structured sections.
    """
    try:
        html = markdown.markdown(file_data["content"])
        soup = BeautifulSoup(html, "html.parser")

        sections = []
        current_heading = "Introduction" # Default heading
        current_text: list[str] = []

        for element in soup.descendants:
            if element.name in ["h1", "h2", "h3"]:
                if current_text:
                    sections.append({
                        "heading": current_heading,
                        "text": " ".join(current_text).strip()
                    })
                    current_text = []
                current_heading = element.get_text().strip()

            elif element.name in ["p", "li", "span"]:
                text = element.get_text().strip()
                if text:
                    current_text.append(text)

        # Flush last section
        if current_text:
            sections.append({
                "heading": current_heading,
                "text": " ".join(current_text).strip()
            })

        return {
            "file_name": file_data["file_name"],
            "source_url": file_data["source_url"],
            "sections": sections
        }
    except Exception as e:
        log.error("Parsing failed", file=file_data.get("file_name"), error=str(e))
        return {}
