from pydantic import BaseModel


class BaseMetadata(BaseModel):
    """Common base model for all document metadata types."""

    def to_json(self, indent: int = 2) -> str:
        """Return JSON string of the metadata with nice formatting."""
        return self.model_dump_json(indent=indent)

    def pretty_print(self):
        """Default fallback print (can be overridden by subclasses)."""
        print(f"📄 Metadata Type: {self.__class__.__name__}")
        print(self.to_json())
