import logging
from typing import List

import pdfplumber

# Silence pdfminer warnings
logging.getLogger("pdfminer").setLevel(logging.ERROR)


class DocumentIngestor:
    def __init__(self, file_path: str):
        """
        Initialize the DocumentIngestor and extract text from the PDF.

        Args:
            file_path (str): Path to the PDF file to ingest.
        """
        self.file_path = file_path
        self.text = self._extract_text()

    def _extract_text(self) -> List[str]:
        """
        Extract text from each page of the PDF.

        Returns:
            List[str]: A list of strings, each representing the text of a page.
        """
        pages_text = []
        with pdfplumber.open(self.file_path) as pdf:
            for page in pdf.pages:
                pages_text.append(page.extract_text() or "")
        return pages_text

    def get_full_text(self) -> str:
        """
        Get the full document text, organized by page.

        Returns:
            str: The concatenated text of all pages, with page markers.
        """
        return "\n".join(
            f"--- Page {i + 1} ---\n{page}" for i, page in enumerate(self.text)
        )
