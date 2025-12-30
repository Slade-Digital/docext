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
            "description": "The primary legal entity name from the 'NAMED INSURED' section. Extract ONLY the main company name BEFORE any 'DBA:', 'D/B/A:', 'aka', or similar indicators. Stop at the first comma, semicolon, or DBA indicator. Example: if the field shows 'Xander Bicycle Corp, DBA: Retrospec Bicycles', extract only 'Xander Bicycle Corp'.",
        },
        {
            "field_name": "dba_names",
            "description": "Extract ONLY the alternate business names that appear AFTER 'DBA:', 'D/B/A:', 'doing business as', 'aka', 'also known as', semicolons, or commas in the named insured field. Do NOT include the primary legal name. Return as comma-separated list. Example: if the field shows 'Xander Bicycle Corp, DBA: Retrospec Bicycles, Critical Cycles', extract 'Retrospec Bicycles, Critical Cycles'. If no DBA indicators are present, return empty string ''.",
        },
        {
            "field_name": "mailing_street",
            "description": "The street address (number and street name) from the mailing address. Example: '123 Main St' or '456 Oak Avenue'. Do not include suite/unit numbers, city, state, or ZIP.",
        },
        {
            "field_name": "mailing_street2",
            "description": "The secondary address line from the mailing address such as suite, unit, apartment, or floor number. Example: 'Suite 200' or 'Unit 5B'. Return empty string '' if not provided.",
        },
        {
            "field_name": "mailing_city",
            "description": "The city name from the mailing address. Example: 'New York' or 'Boston'.",
        },
        {
            "field_name": "mailing_state",
            "description": "The state abbreviation from the mailing address. Example: 'NY' or 'CA'. Use 2-letter state code.",
        },
        {
            "field_name": "mailing_zip",
            "description": "The ZIP code from the mailing address. Example: '10001' or '02134-1234'. Include the full ZIP+4 if present.",
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
        {
            "field_name": "premises_json",
            "description": "Extract ALL premise locations from the 'PREMISES', 'LOCATIONS', or 'SCHEDULE OF LOCATIONS' section as a JSON array. Each premise should be an object with these keys: 'premise_type' (location designation like 'Main Office', 'Branch', or empty string if not stated), 'premise_street' (street address), 'premise_street2' (suite/unit or empty string), 'premise_city', 'premise_state' (2-letter code), 'premise_zip', 'premise_description' (additional notes or empty string). Do NOT include the mailing address from the Named Insured section. Only extract locations explicitly listed in the premises/locations section. If no premises are listed, return empty array []. Example format: [{\"premise_type\": \"Main Office\", \"premise_street\": \"123 Main St\", \"premise_street2\": \"\", \"premise_city\": \"New York\", \"premise_state\": \"NY\", \"premise_zip\": \"10001\", \"premise_description\": \"\"}]",
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
    "accord 📄": [],
}
