from typing import List, Optional

from models.metadata_models.base_metadata import BaseMetadata


class ContractMetadata(BaseMetadata):
    parties: List[str]
    effective_date: Optional[str]
    termination_date: Optional[str]
    key_terms: List[str]

    def pretty_print(self):
        print("📜 Contract Metadata")
        print(f"  🤝 Parties: {', '.join(self.parties) if self.parties else 'N/A'}")
        print(f"  📆 Effective Date: {self.effective_date or 'N/A'}")
        print(f"  🛑 Termination Date: {self.termination_date or 'N/A'}")
        print("  🔑 Key Terms:")
        if self.key_terms:
            for term in self.key_terms:
                print(f"    • {term}")
        else:
            print("    No key terms found.")
