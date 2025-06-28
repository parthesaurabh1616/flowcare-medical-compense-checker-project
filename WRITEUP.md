# Medical Text Compliance Checker – Project Write-up

## Objective
The Medical Text Compliance Checker is a Python-based tool designed to help organizations, healthcare professionals, and regulatory teams ensure that medical product claims and statements comply with the standards set by major regulatory agencies: the FDA (US), EMA (Europe), and HSA (Singapore). The tool aims to prevent the dissemination of misleading, exaggerated, or unsupported claims in medical advertising and product communication, thereby protecting consumers and supporting regulatory compliance.

## Approach & Justification
### Why Rule-Based NLP?
We adopted a **rule-based Natural Language Processing (NLP)** approach for this project. This method leverages regular expressions and keyword matching to identify non-compliant patterns in medical claims. The rationale for this choice includes:
- **Transparency:** All compliance rules are explicit and easy to review or update as regulations evolve.
- **Explainability:** Each non-compliance is directly linked to a specific rule, enabling clear and actionable feedback.
- **Efficiency:** The system is lightweight, fast, and does not require large datasets or model training.
- **Regulatory Alignment:** Regulatory compliance often demands deterministic, auditable logic rather than black-box machine learning models.

### Rule Design
Rules were crafted based on common regulatory restrictions, such as:
- **Absolute claims:** e.g., "guarantees 100% effectiveness", "cures all diseases"
- **Superlative claims:** e.g., "the most advanced", "world's #1", "the best"
- **Unsupported medical claims:** e.g., "will prevent heart attacks", "eliminates all symptoms"
- **Comparative statements:** e.g., "better than all others", "superior to any other"

Each agency (FDA, EMA, HSA) has its own set of rules, but many patterns overlap. The system also detects references to clinical evidence or studies, allowing for a nuanced classification ("Compliant with Evidence") when appropriate.

## Features
- **Multi-agency support:** FDA, EMA, and HSA, each with tailored compliance rules.
- **Binary and nuanced classification:** Returns "Compliant", "Non-Compliant", or "Compliant with Evidence".
- **Detailed explanations:** For non-compliance, the tool highlights the offending phrase and provides a clear explanation.
- **Bulk processing:** Users can upload a CSV file of statements for batch compliance checking.
- **Streamlit web interface:** User-friendly UI for both single and bulk checks.
- **Optional LLM integration:** Users can get a second opinion from OpenAI GPT for complex or ambiguous cases.
- **Extensive test cases:** Over 20 sample statements included for demonstration and validation.

## Implementation Details
- **Core logic:** Implemented in `compliance_checker.py` using Python's `re` module for pattern matching.
- **User interface:** Built with Streamlit (`app.py`), supporting both interactive and bulk CSV-based checks.
- **Testing:** `test_cases.py` runs 15+ sample statements through all agency rules, printing results and explanations.
- **Sample data:** `Statement.csv` and `New Text Document.txt` provide additional real-world test cases.
- **Dependencies:** Managed via `requirements.txt` (Streamlit, pandas, openai).
- **Documentation:** Comprehensive usage and customization instructions in `README.md`.

## Example Workflow
1. **Single Statement Check:**
   - User enters a medical claim in the Streamlit app.
   - Selects the regulatory agency (FDA, EMA, HSA).
   - Receives a compliance status and explanation.
2. **Bulk Check:**
   - User uploads a CSV file with a 'statement' column.
   - The app processes each statement and provides a downloadable results file.
3. **LLM Second Opinion (Optional):**
   - User provides an OpenAI API key.
   - The app queries GPT for a second compliance judgment and explanation.

## Testing & Validation
- The system was tested with over 20 diverse medical claims, covering absolute, superlative, comparative, and evidence-based statements.
- All example inputs from the assessment prompt are included and correctly classified.
- The tool's explanations are clear, actionable, and reference the specific rule violated.

## Future Improvements
- **Expand rule sets:** Incorporate more granular or agency-specific rules as regulations evolve.
- **Add machine learning option:** Integrate a fine-tuned BERT or GPT model for edge cases or to supplement rule-based logic.
- **API deployment:** Provide a REST API for integration with other systems.
- **User management:** Add authentication and usage tracking for enterprise deployment.
- **Automated updates:** Periodically update rules based on regulatory bulletins or user feedback.

## Conclusion
This project delivers a robust, transparent, and user-friendly solution for medical text compliance checking. It empowers users to proactively identify and correct non-compliant claims, reducing regulatory risk and supporting ethical communication in healthcare. 