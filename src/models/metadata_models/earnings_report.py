from typing import Optional, Dict

from models.metadata_models.base_metadata import BaseMetadata


class EarningsReportMetadata(BaseMetadata):
    reporting_period: Optional[str]
    key_metrics: Dict[str, float]
    executive_summary: Optional[str]
