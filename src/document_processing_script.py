import os
import uuid
from pathlib import Path

from core.document_classifier import DocumentClassifier
from core.document_ingestor import DocumentIngestor
from core.metadata_extractor import MetadataExtractor
from llm.utils import get_azure_chat_openai_llm


def run_pipeline(document_path: str) -> dict:
    """ Run the document processing pipeline script."""
    # Create output directory if it doesn't exist
    Path("output").mkdir(exist_ok=True)

    # Generate document ID
    doc_id = str(uuid.uuid4())
    filename = os.path.basename(document_path)

    # Process document
    llm = get_azure_chat_openai_llm()
    ingestor = DocumentIngestor(document_path)
    doc_text = ingestor.get_full_text()

    classifier = DocumentClassifier(llm)
    classification = classifier.classify_document(doc_text)

    extractor = MetadataExtractor(llm)
    metadata = extractor.extract(classification.type.value, doc_text)

    # Create output structure matching app.py format
    result = {
        "document_id": doc_id,
        "filename": filename,
        "classification": classification.model_dump(),
        "metadata": metadata.model_dump() if hasattr(metadata, "model_dump") else metadata,
    }

    # Save to file in output subfolder matching input folder
    input_subfolder = Path(document_path).parent.name
    output_dir = Path("output") / input_subfolder
    output_dir.mkdir(parents=True, exist_ok=True)
    output_filename = output_dir / f"{filename.split('.')[0]}.json"
    with open(output_filename, 'w') as f:
        import json
        json.dump(result, f, indent=2)

    print(f"Saved results to {output_filename}")
    print("Extracted Metadata:")
    if hasattr(metadata, "pretty_print"):
        metadata.pretty_print()

    return result


if __name__ == "__main__":
    # run the pipe for each file in this folder: data/factify
    input_folder = "data/factify"
    for file_path in Path(input_folder).glob("*.pdf"):
        print(f"Processing {file_path}...")
        run_pipeline(file_path)
        print(f"Finished processing {file_path}\n")
