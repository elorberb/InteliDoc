from typing import Optional, List

from pydantic import BaseModel

from models.metadata_models.base_metadata import BaseMetadata


class KeyMetric(BaseModel):
    name: str
    value: float


class EarningsReportMetadata(BaseMetadata):
    reporting_period: Optional[str]
    key_metrics: Optional[List[KeyMetric]] = []
    executive_summary: Optional[str]

    def pretty_print(self):
        print("📊 Earnings Report Metadata")
        print(f"  🗓️ Reporting Period: {self.reporting_period or 'N/A'}")
        print("  📈 Key Metrics:")
        if self.key_metrics:
            for m in self.key_metrics:
                print(f"    • {m.name}: {m.value}")
        else:
            print("    No key metrics found.")
        print("  📝 Executive Summary:")
        print(f"    {self.executive_summary or 'No summary available.'}")
