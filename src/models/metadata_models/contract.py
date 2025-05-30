from typing import List, Optional

from models.metadata_models.base_metadata import BaseMetadata


class ContractMetadata(BaseMetadata):
    parties: List[str]
    effective_date: Optional[str]
    termination_date: Optional[str]
    key_terms: List[str]
