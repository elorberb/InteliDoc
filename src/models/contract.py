from typing import List, Optional

from pydantic import BaseModel


class ContractMetadata(BaseModel):
    parties: List[str]
    effective_date: Optional[str]
    termination_date: Optional[str]
    key_terms: List[str]
