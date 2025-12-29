from __future__ import annotations

TEMPLATES_FIELDS = {
    "invoice colab demo 🧾": [
        {"field_name": "invoice_number", "description": "Invoice number"},
        {"field_name": "invoice_date", "description": "Invoice date"},
        {"field_name": "invoice_amount", "description": "Invoice amount"},
        {
            "field_name": "seller_name",
            "description": "Seller name. If not explicitly mentioned, return ''",
        },
    ],
    "invoice 🧾": [
        {"field_name": "invoice_number", "description": "Invoice number"},
        {"field_name": "invoice_date", "description": "Invoice date"},
        {"field_name": "invoice_amount", "description": "Invoice amount"},
        {
            "field_name": "invoice_currency",
            "description": "Invoice currency. If not explicitly mentioned, return ''",
        },
        {
            "field_name": "document_type",
            "description": "Document type. If not explicitly mentioned, return ''",
        },
        {
            "field_name": "seller_name",
            "description": "Seller name. If not explicitly mentioned, return ''",
        },
        {"field_name": "buyer_name", "description": "Buyer name"},
        {"field_name": "seller_address", "description": "Seller address"},
        {"field_name": "buyer_address", "description": "Buyer address"},
        {"field_name": "seller_tax_id", "description": "Seller tax id"},
        {"field_name": "buyer_tax_id", "description": "Buyer tax id"},
    ],
    "passport 🎫": [
        {"field_name": "full_name", "description": "Full name"},
        {
            "field_name": "date_of_birth",
            "description": "Date of birth. Return in format YYYY-MM-DD",
        },
        {"field_name": "passport_number", "description": "Passport number"},
        {"field_name": "passport_type", "description": "Passport type"},
        {
            "field_name": "date_of_issue",
            "description": "Date of issue. Return in format YYYY-MM-DD",
        },
        {
            "field_name": "date_of_expiry",
            "description": "Date of expiry. Return in format YYYY-MM-DD",
        },
        {"field_name": "place_of_birth", "description": "Place of birth"},
        {"field_name": "nationality", "description": "Nationality"},
        {"field_name": "gender", "description": "Gender"},
    ],
    "accord 📄": [
        {
            "field_name": "insured_name",
            "description": "The full legal name of the named insured from the 'NAMED INSURED' section. Extract only the name, do not include the address.",
        },
        {
            "field_name": "mailing_address",
            "description": "The complete mailing address of the named insured including street address, city, state, and ZIP code. Do not include the name, only the address.",
        },
        {
            "field_name": "proposed_eff_date",
            "description": "The proposed effective date found in the 'POLICY PERIOD' section, usually labeled as 'FROM' or 'Effective Date'. Return in MM/DD/YYYY format.",
        },
        {
            "field_name": "proposed_exp_date",
            "description": "The proposed expiration date found in the 'POLICY PERIOD' section, usually labeled as 'TO' or 'Expiration Date'. Return in MM/DD/YYYY format.",
        },
        {
            "field_name": "business_phone",
            "description": "The business phone number of the insured party, may be labeled as 'Business Phone', 'Phone', 'Tel', or in the contact information section. Return in standard phone format.",
        },
        {
            "field_name": "primary_business_operations",
            "description": "The description of the insured's primary business operations or business type, typically found in the 'DESCRIPTION OF OPERATIONS' section or 'Business Description' field. Include the complete business activity description.",
        },
    ],
}

TEMPLATES_TABLES = {
    "invoice colab demo 🧾": [
        {
            "field_name": "items_description",
            "description": "Description of the product",
        },
        {"field_name": "Unit Price", "description": "Unit price of the product"},
    ],
    "invoice 🧾": [
        {"field_name": "Quantity", "description": "Total quantity of the product"},
        {
            "field_name": "items_description",
            "description": "Description of the product",
        },
        {"field_name": "Unit Price", "description": "Unit price of the product"},
        {"field_name": "Total Price", "description": "Total price of the product"},
        {"field_name": "tax", "description": "tax amount"},
    ],
    "accord 📄": [
        {
            "field_name": "premise_address",
            "description": "Extract only the street address, city, state, and ZIP code from each premise location. Do NOT include descriptors like 'Main Office' or 'Main Garage' - only the physical address.",
        },
        {
            "field_name": "premise_type",
            "description": "Extract the location type or designation (such as 'Main Office', 'Main Garage', 'Branch', 'Warehouse') if present in the premise information. If the cell only contains an address with no type designation, return empty string.",
        },
        {
            "field_name": "premise_building_number",
            "description": "The building number, unit number, or suite number associated with the premise, if specified. Return empty string if not provided.",
        },
        {
            "field_name": "premise_description",
            "description": "Any additional description or notes about the premise location beyond the type and address. Return empty string if not provided.",
        },
    ],
}
