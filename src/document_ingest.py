from typing import List, Dict

import pdfplumber


class DocumentIngestor:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.text = self._extract_text()

    def _extract_text(self) -> List[str]:
        pages_text = []
        with pdfplumber.open(self.file_path) as pdf:
            for page in pdf.pages:
                pages_text.append(page.extract_text() or "")
        return pages_text

    def extract_relevant_info(self, keywords: List[str]) -> Dict[str, List[str]]:
        relevant = {kw: [] for kw in keywords}
        for page_num, page_text in enumerate(self.text):
            for kw in keywords:
                if kw.lower() in page_text.lower():
                    relevant[kw].append(f"Page {page_num + 1}: {page_text}")
        return relevant

    def get_full_text(self) -> str:
        """Returns the full document text, organized by page, as a single string."""
        return "\n".join(
            f"--- Page {i + 1} ---\n{page}" for i, page in enumerate(self.text)
        )


if __name__ == '__main__':
    # test the test extraction
    ingestor = DocumentIngestor("data/invoice2.pdf")
    print("Extracted Text:")
    for i, page in enumerate(ingestor.text):
        print(f"Page {i + 1}:\n{page}\n")
