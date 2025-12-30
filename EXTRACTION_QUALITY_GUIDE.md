# Guide: Maintaining Extraction Quality at Scale

## Problem Statement
As extraction complexity increases (more fields, longer prompts), VLM quality degrades due to:
- Attention dilution across many fields
- Context window saturation
- Position bias (later fields get worse results)
- Field interaction effects

## Solutions by Category

### 1. Model Configuration Tuning

#### A. Increase Max Tokens for Output
```python
# In docext/core/client.py, line 12
max_tokens: int = 5000  # Current default

# Recommendation: Increase for complex extractions
max_tokens: int = 8000  # For templates with 10-15 fields
max_tokens: int = 12000 # For templates with 15+ fields or JSON arrays
```

**Why**: Complex JSON outputs (like premises_json array) need more tokens. If truncated mid-JSON, parsing fails.

#### B. Enable Guided JSON (Currently Commented Out)
```python
# In docext/core/client.py, lines 38-41
# Uncomment and test for better JSON reliability:
elif model_name.startswith("hosted_vllm/") and format:
    completion_args["guided_json"] = format
    if "qwen" in model_name.lower():
        completion_args["guided_backend"] = "xgrammar:disable-any-whitespace"
```

**Why**: Guided JSON forces the model to output valid JSON structure, reducing parsing errors.

#### C. Sampling Parameters
```python
# In docext/core/client.py, add these to completion_args:
"top_p": 0.95,           # Slightly increase diversity (default: 1.0)
"repetition_penalty": 1.1 # Prevent repeating same value across fields
```

---

### 2. Prompt Engineering Strategies

#### A. Field Prioritization (What You Just Did)
```python
# Order fields by:
# 1. Importance (critical fields first)
# 2. Simplicity (simple extractions before complex ones)
# 3. Logical grouping (related fields together)

TEMPLATES_FIELDS["accord"] = [
    # High priority, simple
    {"field_name": "insured_name", ...},
    {"field_name": "dba_names", ...},
    {"field_name": "business_phone", ...},

    # Medium priority, structured
    {"field_name": "mailing_street", ...},
    # ... other address fields

    # Complex, can tolerate errors
    {"field_name": "premises_json", ...},  # Last
]
```

#### B. Concise Descriptions
**Current Issue**: Some descriptions are 300+ characters
```python
# Before (337 chars)
"description": "The legal business name from the Named Insured field, stopping before any explicit DBA indicator. Extract everything before 'DBA:', 'DBA', 'D/B/A:', 'D/B/A', 'doing business as', or 'aka'. Include commas if they are part of the legal entity name (e.g., 'Acme, LLC'). Do not include alternate business names."

# After (shorter, clearer)
"description": "Legal business name from Named Insured, before any DBA/D/B/A/aka indicator. Include commas in entity names (e.g., 'Acme, LLC')."
```

**Recommendation**: Keep descriptions under 150 characters when possible.

#### C. Few-Shot Examples (Advanced)
Add example extractions to the prompt:
```python
# In prompts.py, modify get_fields_messages()
example_text = """
Example extraction:
Document shows: "ABC Corp, DBA: XYZ Inc"
insured_name: "ABC Corp"
dba_names: "XYZ Inc"
"""
# Add to messages before the actual extraction request
```

---

### 3. Architectural Patterns

#### A. **Chunked Extraction** (Recommended for 15+ fields)
Split extraction into multiple API calls:

```python
# Create separate extraction groups
GROUP_1_FIELDS = ["insured_name", "dba_names", "phone", ...]  # Critical
GROUP_2_FIELDS = ["mailing_street", "mailing_city", ...]      # Address
GROUP_3_FIELDS = ["premises_json"]                             # Complex

# Run 3 separate extractions, merge results
def extract_with_chunking(file_path, model_name):
    results = {}

    # Extract critical fields
    results.update(extract_fields(file_path, model_name, GROUP_1_FIELDS))

    # Extract address fields
    results.update(extract_fields(file_path, model_name, GROUP_2_FIELDS))

    # Extract complex fields
    results.update(extract_fields(file_path, model_name, GROUP_3_FIELDS))

    return results
```

**Pros**: Each extraction is focused, higher quality
**Cons**: 3x API calls = 3x cost/time

#### B. **Cascading Extraction** (Best for Critical Fields)
Extract in stages with confidence-based retry:

```python
def extract_with_cascade(file_path, model_name):
    # Stage 1: Extract all fields
    results = extract_all_fields(file_path, model_name)

    # Stage 2: Re-extract low-confidence fields individually
    low_conf_fields = [f for f, v in results.items() if v['confidence'] < 70]

    for field in low_conf_fields:
        # Re-extract just this one field with focused prompt
        retry_result = extract_single_field(file_path, model_name, field)
        if retry_result['confidence'] > results[field]['confidence']:
            results[field] = retry_result

    return results
```

#### C. **Specialized Extraction Chains**
Use different prompts for different field types:

```python
# Simple field extraction (name, phone, dates)
simple_fields = extract_simple_fields(doc)

# Structured extraction (addresses)
addresses = extract_structured_data(doc, "address")

# Complex reasoning (DBA splitting, premises)
complex_fields = extract_with_reasoning(doc)

# Merge results
final_result = {**simple_fields, **addresses, **complex_fields}
```

---

### 4. Post-Processing Fallbacks

#### A. **Regex-Based Validation & Correction**
```python
import re

def validate_and_fix_phone(extracted_phone):
    """Fallback: Extract phone with regex if VLM fails"""
    if not extracted_phone or len(extracted_phone) < 10:
        # Search in the original document text
        phone_pattern = r'\(?(\d{3})\)?[-.\s]?(\d{3})[-.\s]?(\d{4})'
        match = re.search(phone_pattern, document_text)
        if match:
            return f"({match.group(1)}) {match.group(2)}-{match.group(3)}"
    return extracted_phone

def validate_and_fix_dba(insured_name, dba_names):
    """Fallback: Split DBA programmatically if VLM fails"""
    if not dba_names and any(keyword in insured_name.lower()
                            for keyword in ['dba', 'd/b/a', 'aka']):
        # Split programmatically
        for separator in [' DBA:', ' DBA ', ' D/B/A:', ', ']:
            if separator in insured_name:
                parts = insured_name.split(separator, 1)
                return parts[0].strip(), parts[1].strip()
    return insured_name, dba_names
```

#### B. **Confidence-Based Human Review Triggers**
```python
def should_flag_for_review(extraction_results, thresholds):
    """Determine if extraction needs human review"""
    flags = []

    # Flag low-confidence critical fields
    critical_fields = ['insured_name', 'business_phone', 'eff_date']
    for field in critical_fields:
        if extraction_results[field]['confidence'] < thresholds['critical']:
            flags.append(f"Low confidence on critical field: {field}")

    # Flag missing required fields
    required_fields = ['insured_name', 'mailing_street', 'eff_date']
    for field in required_fields:
        if not extraction_results[field]['value']:
            flags.append(f"Missing required field: {field}")

    # Flag hallucination indicators
    if extraction_results['premise_type']['value'] and \
       'main office' in extraction_results['premise_type']['value'].lower():
        flags.append("Possible hallucination: premise_type='Main Office'")

    return flags
```

---

### 5. Model Selection Strategy

#### Current Model: Qwen2.5-VL-7B-Instruct-AWQ
- Good for: Cost-effective, fast
- Limitations: 7B parameters, quantized (AWQ reduces precision)

#### Upgrade Path for Better Quality:

| Model | Size | When to Use |
|-------|------|-------------|
| **Qwen2.5-VL-7B-Instruct** | 7B | Current production (non-AWQ version = higher quality) |
| **Qwen2.5-VL-32B-Instruct-AWQ** | 32B | Complex documents, 15+ fields |
| **GPT-4o / Claude 3.5 Sonnet** | Closed | Critical documents, highest accuracy needed |
| **Gemini 2.0 Flash** | Closed | Fast + accurate, good cost/performance |

```bash
# To upgrade model:
python -m docext.app.app --model_name hosted_vllm/Qwen/Qwen2.5-VL-32B-Instruct-AWQ
# Requires 48GB VRAM
```

---

### 6. Image Preprocessing

#### A. Increase Image Quality
```python
# In docext/core/extract.py
# Current: max_img_size parameter
resize_images(file_paths, max_img_size)

# Recommendation:
max_img_size = 2048  # Default is often 1024
# Larger images = better text recognition, but slower inference
```

#### B. Document Enhancement
```python
from PIL import Image, ImageEnhance

def preprocess_document_image(img_path):
    """Enhance document image before extraction"""
    img = Image.open(img_path)

    # Increase contrast for faded documents
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(1.5)

    # Sharpen for blurry scans
    enhancer = ImageEnhance.Sharpness(img)
    img = enhancer.enhance(2.0)

    return img
```

---

## Recommended Implementation Plan

### Phase 1: Quick Wins (Immediate)
1. ✅ **Reorder fields** (already done)
2. **Shorten field descriptions** to <150 chars
3. **Increase max_tokens** to 8000-12000
4. **Add post-processing fallbacks** for phone and DBA

### Phase 2: Quality Improvements (This Week)
5. **Enable guided JSON** for premises_json
6. **Add confidence thresholds** for review flagging
7. **Implement regex validation** for structured fields (phone, zip)

### Phase 3: Scaling (Future)
8. **Chunked extraction** for templates with 20+ fields
9. **Upgrade to non-AWQ model** (7B regular or 32B AWQ)
10. **A/B test** different prompt formats

---

## Monitoring & Testing

### Key Metrics to Track
```python
extraction_metrics = {
    "field_extraction_rate": 0.95,      # % of fields successfully extracted
    "avg_confidence": 87.3,              # Average confidence across all fields
    "review_rate": 0.12,                 # % of extractions flagged for review
    "dba_split_accuracy": 0.78,          # % of DBAs correctly separated
    "premise_hallucination_rate": 0.15,  # % of premises with invented types
}
```

### Testing Checklist
- [ ] Test with 10+ real documents
- [ ] Track confidence scores per field
- [ ] Measure extraction time
- [ ] Count hallucinations (invented values)
- [ ] Validate all phone numbers with regex
- [ ] Check all JSON fields parse correctly

---

## Quick Reference: Configuration Changes

```python
# docext/core/client.py - Increase output capacity
max_tokens: int = 12000  # Line 12

# docext/core/vllm.py - Increase context window
max_model_len: int = 32000  # Line 17 (if model supports it)

# Add to client.py completion_args for better sampling
"top_p": 0.95,
"repetition_penalty": 1.1,
```
