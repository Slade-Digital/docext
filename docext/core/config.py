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
            "field_name": "dba_names",
            "description": "All 'Doing Business As' (DBA) names, trade names, or alternate business names associated with the named insured. Look for indicators like 'DBA:', 'D/B/A:', 'doing business as', 'aka', 'also known as', or additional company names after semicolons, commas, or in parentheses following the legal name. Return as comma-separated list if multiple DBAs exist, or return empty string '' if no DBAs are present.",
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
            "field_name": "premise_type",
            "description": "Extract the location type or designation (such as 'Main Office', 'Main Garage', 'Branch', 'Warehouse') if present in the premise information. If the cell only contains an address with no type designation, return empty string.",
        },
        {
            "field_name": "premise_street",
            "description": "The street address (number and street name) from each premise location. Example: '123 Main St' or '456 Oak Avenue'. Do not include suite/unit numbers, city, state, or ZIP.",
        },
        {
            "field_name": "premise_street2",
            "description": "The secondary address line such as suite, unit, building, or floor number. Example: 'Suite 200' or 'Bldg 1'. Return empty string if not provided.",
        },
        {
            "field_name": "premise_city",
            "description": "The city name from the premise address. Example: 'New York' or 'Boston'.",
        },
        {
            "field_name": "premise_state",
            "description": "The state abbreviation from the premise address. Example: 'NY' or 'CA'. Use 2-letter state code.",
        },
        {
            "field_name": "premise_zip",
            "description": "The ZIP code from the premise address. Example: '10001' or '02134-1234'. Include the full ZIP+4 if present.",
        },
        {
            "field_name": "premise_description",
            "description": "Any additional description or notes about the premise location beyond the type and address. Return empty string if not provided.",
        },
    ],
}
