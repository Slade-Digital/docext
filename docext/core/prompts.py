from __future__ import annotations

import pandas as pd
from PIL import Image

from docext.core.utils import encode_image


def _get_name_desc_prompt(fields: list[str], fields_description: list[str]) -> str:
    return "\n".join(
        [
            f"{field.replace(' ', '_').lower()}: {description}"
            for field, description in zip(fields, fields_description)
        ],
    )


def _get_fields_output_format(fields: list[str]) -> dict:
    return {field.replace(" ", "_").lower(): "..." for field in fields}


def get_fields_messages(
    fields: list[str],
    fields_description: list[str],
    filepaths: list[str],
) -> list[dict]:
    messages = [
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": f"Extract the following fields from the documents:\n {_get_name_desc_prompt(fields, fields_description)}.",
                },
                {"type": "text", "text": f"Documents:\n"},
                *[
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{encode_image(filepath)}",
                        },
                    }
                    for filepath in filepaths
                ],
                {
                    "type": "text",
                    "text": f"Return a JSON with the following format:\n {_get_fields_output_format(fields)}. If a field is not found, return '' for that field. Do not give any explanation.",
                },
            ],
        },
    ]
    return messages


def _get_tables_output_format(columns: list[str]) -> str:
    return pd.DataFrame({col: [".."] for col in columns}).to_markdown(index=False)


def get_tables_messages(
    columns_names: list[str],
    columns_description: list[str],
    filepaths: list[str],
) -> list[dict]:
    messages = [
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": f"Extract the following columns from the documents:\n {_get_name_desc_prompt(columns_names, columns_description)}.",
                },
                {"type": "text", "text": f"Documents:\n"},
                *[
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{encode_image(filepath)}",
                        },
                    }
                    for filepath in filepaths
                ],
                {
                    "type": "text",
                    "text": f"Return ONLY ONE table in markdown format with exactly these columns:\n {_get_tables_output_format(columns_names)}.\n\nIMPORTANT:\n- Return ONLY the requested table, not all tables in the document\n- Use exactly {len(columns_names)} columns as specified\n- If a cell is not found, return '' for that column\n- If the table does not exist in the document, return an empty table with just the header row\n- Do not include any other tables, explanations, or text",
                },
            ],
        },
    ]
    return messages
