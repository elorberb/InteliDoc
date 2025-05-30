from typing import Optional, Dict

from pydantic import BaseModel


class EarningsReportMetadata(BaseModel):
    reporting_period: Optional[str]
    key_metrics: Dict[str, float]
    executive_summary: Optional[str]
