"""
JSON Formatter for Docext Extraction Results

This module converts Docext's DataFrame outputs into structured JSON
for use in downstream insurance processing systems.

Usage:
    from docext_json_formatter import format_extraction_json

    fields_df, tables_df = docext.extract_information(...)
    json_result = format_extraction_json(fields_df, tables_df, doc_type="accord")
"""

from datetime import datetime
from typing import Dict, List, Any, Optional
import pandas as pd


def format_extraction_json(
    fields_df: pd.DataFrame,
    tables_df: pd.DataFrame,
    doc_type: str = "unknown",
    submission_id: Optional[str] = None,
    metadata: Optional[Dict[str, Any]] = None,
    confidence_threshold: int = 70,
) -> Dict[str, Any]:
    """
    Convert Docext extraction results to structured JSON.

    Args:
        fields_df: DataFrame with columns [fields, answer, confidence, document_index]
        tables_df: DataFrame with extracted table data
        doc_type: Document type (e.g., "accord", "certificate", "policy")
        submission_id: Optional submission identifier
        metadata: Optional additional metadata
        confidence_threshold: Threshold below which fields are flagged for review

    Returns:
        Structured JSON dictionary
    """
    result = {
        "submission_id": submission_id,
        "document_type": doc_type,
        "extraction_metadata": {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "fields_count": len(fields_df) if not fields_df.empty else 0,
            "tables_count": len(tables_df) if not tables_df.empty else 0,
            **(metadata or {})
        },
        "fields": {},
        "tables": {},
        "quality_metrics": {}
    }

    # Process fields
    if not fields_df.empty:
        confidences = []
        low_confidence_fields = []
        missing_fields = []

        for _, row in fields_df.iterrows():
            field_name = row['fields']
            field_value = row['answer']
            field_confidence = row['confidence']

            result["fields"][field_name] = {
                "value": field_value,
                "confidence": field_confidence
            }

            # Track metrics
            if isinstance(field_confidence, (int, float)):
                confidences.append(field_confidence)
                if field_confidence < confidence_threshold:
                    low_confidence_fields.append(field_name)

            if not field_value or field_value == "":
                missing_fields.append(field_name)

        # Calculate quality metrics
        avg_confidence = sum(confidences) / len(confidences) if confidences else 0
        result["quality_metrics"] = {
            "average_confidence": round(avg_confidence, 2),
            "low_confidence_fields": low_confidence_fields,
            "missing_fields": missing_fields,
            "requires_review": len(low_confidence_fields) > 0 or len(missing_fields) > 0
        }

    # Process tables
    if not tables_df.empty:
        # Convert table DataFrame to list of dictionaries
        result["tables"]["data"] = tables_df.to_dict(orient="records")
        result["extraction_metadata"]["table_rows"] = len(tables_df)

    return result


def format_extraction_json_flat(
    fields_df: pd.DataFrame,
    tables_df: pd.DataFrame,
    doc_type: str = "unknown",
    submission_id: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Convert Docext extraction results to flat JSON (better for databases).

    Args:
        fields_df: DataFrame with columns [fields, answer, confidence, document_index]
        tables_df: DataFrame with extracted table data
        doc_type: Document type (e.g., "accord", "certificate", "policy")
        submission_id: Optional submission identifier

    Returns:
        Flat JSON dictionary with field_name and field_name_confidence keys
    """
    result = {
        "submission_id": submission_id,
        "document_type": doc_type,
        "extraction_timestamp": datetime.utcnow().isoformat() + "Z",
    }

    # Add fields as flat key-value pairs
    if not fields_df.empty:
        confidences = []

        for _, row in fields_df.iterrows():
            field_name = row['fields']
            field_value = row['answer']
            field_confidence = row['confidence']

            # Add field value
            result[field_name] = field_value

            # Add confidence as separate key
            result[f"{field_name}_confidence"] = field_confidence

            if isinstance(field_confidence, (int, float)):
                confidences.append(field_confidence)

        # Add average confidence
        if confidences:
            result["average_confidence"] = round(sum(confidences) / len(confidences), 2)

    # Add tables as nested array
    if not tables_df.empty:
        result["tables"] = tables_df.to_dict(orient="records")

    return result


def format_for_insurance_system(
    fields_df: pd.DataFrame,
    tables_df: pd.DataFrame,
    doc_type: str = "accord",
    submission_id: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Format extraction results specifically for insurance clearance systems.

    Organizes data by insurance-specific concerns:
    - Policy information
    - Insured party information
    - Premises/locations
    - Coverage details

    Args:
        fields_df: DataFrame with extraction results
        tables_df: DataFrame with table data
        doc_type: Document type
        submission_id: Submission identifier

    Returns:
        Insurance-system-optimized JSON structure
    """
    result = {
        "submission_id": submission_id,
        "document_type": doc_type,
        "extracted_at": datetime.utcnow().isoformat() + "Z",
        "policy_info": {},
        "insured_party": {},
        "premises": [],
        "business_info": {},
        "metadata": {}
    }

    # Map fields to insurance categories
    if not fields_df.empty:
        import json

        for _, row in fields_df.iterrows():
            field_name = row['fields']
            field_value = row['answer']
            field_confidence = row['confidence']

            # Handle premises_json specially
            if field_name == 'premises_json':
                try:
                    # Parse the JSON array from the field
                    if field_value and field_value.strip():
                        premises_list = json.loads(field_value)
                        if isinstance(premises_list, list):
                            result["premises"] = premises_list
                        else:
                            result["premises"] = []
                    else:
                        result["premises"] = []
                except (json.JSONDecodeError, ValueError):
                    # If JSON parsing fails, store as empty array
                    result["premises"] = []
                    result["metadata"]["premises_parse_error"] = {
                        "value": field_value,
                        "confidence": field_confidence
                    }
                continue

            field_data = {
                "value": field_value,
                "confidence": field_confidence
            }

            # Categorize by field name
            if 'eff_date' in field_name or 'exp_date' in field_name:
                result["policy_info"][field_name] = field_data
            elif (
                'insured_name' in field_name
                or 'dba_names' in field_name
                or 'mailing_' in field_name
                or 'phone' in field_name
            ):
                result["insured_party"][field_name] = field_data
            elif 'business' in field_name or 'operations' in field_name:
                result["business_info"][field_name] = field_data
            else:
                result["metadata"][field_name] = field_data

    # Legacy: Add premises from table (if using old table-based extraction)
    if not tables_df.empty and not result["premises"]:
        result["premises"] = tables_df.to_dict(orient="records")

    return result


# Example usage
if __name__ == "__main__":
    import pandas as pd

    # Sample data
    fields_df = pd.DataFrame([
        {"fields": "insured_name", "answer": "Acme Corp", "confidence": 95, "document_index": 0},
        {"fields": "mailing_address", "answer": "123 Main St, NY 10001", "confidence": 98, "document_index": 0},
        {"fields": "proposed_eff_date", "answer": "01/01/2025", "confidence": 100, "document_index": 0},
        {"fields": "business_phone", "answer": "(555) 123-4567", "confidence": 65, "document_index": 0},
    ])

    tables_df = pd.DataFrame([
        {"premise_address": "123 Main St", "premise_type": "Main Office", "premise_building_number": "Bldg 1", "premise_description": "HQ"},
    ])

    # Format 1: Nested structure
    json_nested = format_extraction_json(fields_df, tables_df, doc_type="accord", submission_id="SUB-123")
    print("Nested JSON:")
    import json
    print(json.dumps(json_nested, indent=2))

    print("\n" + "="*50 + "\n")

    # Format 2: Flat structure
    json_flat = format_extraction_json_flat(fields_df, tables_df, doc_type="accord", submission_id="SUB-123")
    print("Flat JSON:")
    print(json.dumps(json_flat, indent=2))

    print("\n" + "="*50 + "\n")

    # Format 3: Insurance-specific
    json_insurance = format_for_insurance_system(fields_df, tables_df, doc_type="accord", submission_id="SUB-123")
    print("Insurance System JSON:")
    print(json.dumps(json_insurance, indent=2))
