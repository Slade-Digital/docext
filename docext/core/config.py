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
            "description": "The legal business name from the Named Insured field, stopping before any explicit DBA indicator. Extract everything before 'DBA:', 'DBA', 'D/B/A:', 'D/B/A', 'doing business as', or 'aka'. Include commas if they are part of the legal entity name (e.g., 'Acme, LLC'). Do not include alternate business names.",
        },
        {
            "field_name": "dba_names",
            "description": "Alternate business names that appear after DBA indicators in the Named Insured field. Extract all names that come after 'DBA:', 'DBA', 'D/B/A:', 'D/B/A', 'doing business as', or 'aka'. If multiple DBAs are listed, separate them with commas. If no DBA indicator exists, return ''.",
        },
        {
            "field_name": "business_phone",
            "description": "The business phone number found anywhere on the form, including in the Named Insured section, contact information area, or phone fields. Look for labels like 'Phone', 'Tel', 'Business Phone', or phone number patterns like (XXX) XXX-XXXX. If multiple numbers exist, use the primary business number. If not found, return ''.",
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
            "field_name": "primary_business_operations",
            "description": "The description of the insured's primary business operations or business type, typically found in the 'DESCRIPTION OF OPERATIONS' section or 'Business Description' field. Include the complete business activity description.",
        },
        {
            "field_name": "premises_json",
            "description": "Extract ALL premise locations from sections labeled 'PREMISES', 'LOCATIONS', or 'SCHEDULE OF LOCATIONS' as a JSON array. Each premise must be an object with keys: 'premise_type' (ONLY if text like 'Main Office', 'Branch', 'Warehouse' is explicitly visible next to the address, otherwise use empty string), 'premise_street', 'premise_street2', 'premise_city', 'premise_state', 'premise_zip', 'premise_description'. CRITICAL: Do NOT include the mailing address. Do NOT invent or assume premise_type values - only use what is explicitly written. If the premises section only shows an address without a type label, use empty string for premise_type. Return empty array [] if no premises section exists.",
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
