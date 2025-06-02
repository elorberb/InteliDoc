import os
import uuid
from pathlib import Path

from document_classifier import DocumentClassifier
from document_ingestor import DocumentIngestor
from llm_utils import get_azure_chat_openai_llm
from metadata_extractor import MetadataExtractor
from models.analyze_response import AnalyzeResponse


def run_pipeline(document_path):
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
        "metadata": metadata.model_dump()
    }

    # Save to file
    output_filename = f"output/{filename.split('.')[0]}.json"
    with open(output_filename, 'w') as f:
        import json
        json.dump(result, f, indent=2)

    print(f"Saved results to {output_filename}")
    print("Extracted Metadata:")
    metadata.pretty_print()

    return result


if __name__ == "__main__":
    # run the pipe for each file in this folder: data/factify
    input_folder = "data/factify"
    for file_path in Path(input_folder).glob("*.pdf"):
        print(f"Processing {file_path}...")
        run_pipeline(file_path)
        print(f"Finished processing {file_path}\n")