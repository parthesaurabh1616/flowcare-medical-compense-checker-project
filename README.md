# Medical Text Compliance Checker

## Overview
This project implements a rule-based compliance checker for medical product claims, ensuring they meet regulatory standards set by the FDA (US), EMA (Europe), and HSA (Singapore). The system classifies input text as Compliant or Non-Compliant and provides explanations for non-compliance.

## Approach & Justification
A rule-based NLP approach was chosen for transparency, explainability, and ease of tuning. The system uses regular expressions and keyword matching to detect non-compliant patterns such as absolute claims, superlatives, unsupported medical claims, and comparative statements. This method is effective for regulatory compliance, where explicit rules are preferable to black-box models.

## Files
- `compliance_checker.py`: Core compliance checking logic.
- `test_cases.py`: Script with 15 sample statements tested against all agencies.
- `app.py`: Streamlit UI for user-friendly compliance checking.
- `requirements.txt`: Dependencies for running the scripts and UI.

## Usage
1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
2. **Run test cases:**
   ```bash
   python test_cases.py
   ```
3. **Launch Streamlit app:**
   ```bash
   streamlit run app.py
   ```

## Example
- Input: `This drug guarantees 100% effectiveness in curing diabetes.`
- Output: Non-Compliant
- Explanation: Absolute claims are not allowed.

## Customization
- Expand or modify rules in `compliance_checker.py` to adapt to new regulations or agency-specific requirements.

---
**Author:** AI Engineer Assessment Submission 