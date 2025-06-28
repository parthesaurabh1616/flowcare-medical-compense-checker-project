import re
from typing import List, Tuple, Dict
import os

# LLM integration
try:
    import openai
except ImportError:
    openai = None

# Define agency-specific rules and explanations
AGENCY_RULES = {
    "FDA": [
        (r"guarantees?\\b|100%|cure[s]?\\b", "Absolute claims are not allowed (FDA)."),
        (r"most (advanced|effective|powerful|potent|innovative|trusted)|best(?! practice)|better than all others|world'?s? (best|leading|#1|number one)", "Superlative claims need supporting evidence (FDA)."),
        (r"will (prevent|stop|eliminate|cure)|prevents? (disease|illness|condition)|treats? (all|every|any)", "Medical claims require proper disclaimers or evidence (FDA)."),
        (r"better than (all|any|other|others)|superior to", "Comparative claims must be evidence-based (FDA)."),
    ],
    "EMA": [
        (r"guarantees?\\b|100%|cure[s]?\\b", "Absolute claims are not allowed (EMA)."),
        (r"most (advanced|effective|powerful|potent|innovative|trusted)|best(?! practice)|better than all others|world'?s? (best|leading|#1|number one)", "Superlative claims need supporting evidence (EMA)."),
        (r"will (prevent|stop|eliminate|cure)|prevents? (disease|illness|condition)|treats? (all|every|any)", "Medical claims require proper disclaimers or evidence (EMA)."),
        (r"better than (all|any|other|others)|superior to", "Comparative claims must be evidence-based (EMA)."),
    ],
    "HSA": [
        (r"guarantees?\\b|100%|cure[s]?\\b", "Absolute claims are not allowed (HSA)."),
        (r"most (advanced|effective|powerful|potent|innovative|trusted)|best(?! practice)|better than all others|world'?s? (best|leading|#1|number one)", "Superlative claims need supporting evidence (HSA)."),
        (r"will (prevent|stop|eliminate|cure)|prevents? (disease|illness|condition)|treats? (all|every|any)", "Medical claims require proper disclaimers or evidence (HSA)."),
        (r"better than (all|any|other|others)|superior to", "Comparative claims must be evidence-based (HSA)."),
    ],
}

# Evidence citation patterns
EVIDENCE_PATTERNS = [
    r"according to (a|an|the)? ?(\d{4})? ?(study|trial|report|paper|article|publication|data|evidence)",
    r"published in (the )?[A-Za-z ]+ (journal|magazine|review|proceedings)",
    r"(randomized|double-blind|placebo-controlled) (study|trial)",
    r"(meta-analysis|systematic review)",
    r"(as shown|as demonstrated|as reported) in (a|an|the)? ?(study|trial|report|publication)",
]

def check_compliance(text: str, agency: str = "FDA") -> Tuple[str, List[Dict]]:
    """
    Checks if the input text is compliant with the selected agency's rules.
    Returns ("Compliant"/"Non-Compliant"/"Compliant with Evidence", list of dicts with explanation and offending phrase)
    """
    text_lower = text.lower()
    agency = agency.upper()
    rules = AGENCY_RULES.get(agency, AGENCY_RULES["FDA"])
    violations = []
    for pattern, explanation in rules:
        for match in re.finditer(pattern, text_lower):
            offending = text[match.start():match.end()]
            violations.append({
                "explanation": explanation,
                "phrase": offending
            })
    # Evidence detection
    evidence_found = False
    for epat in EVIDENCE_PATTERNS:
        if re.search(epat, text_lower):
            evidence_found = True
            break
    # If evidence is found and there are violations, downgrade severity
    if evidence_found and violations:
        return "Compliant with Evidence", [
            {"explanation": "Claim references supporting evidence. Please ensure evidence is robust and cited properly.", "phrase": "evidence citation"}
        ] + violations
    # If text mentions clinical studies or evidence, mark as compliant (unless violations found)
    if not violations and (evidence_found or re.search(r"clinical (studies|trials|evidence|data)", text_lower)):
        return "Compliant", [{"explanation": "Backed by clinical trial data or evidence.", "phrase": "clinical studies/trials/evidence/data"}]
    if not violations:
        return "Compliant", [{"explanation": "No non-compliant patterns detected.", "phrase": ""}]
    return "Non-Compliant", violations

def llm_compliance_check(text: str, agency: str = "FDA", api_key: str = None) -> Tuple[str, str]:
    """
    Uses OpenAI GPT to provide a compliance judgment and explanation.
    Returns (status, explanation)
    """
    if openai is None:
        return "LLM not available", "OpenAI package not installed."
    api_key = api_key or os.getenv("OPENAI_API_KEY")
    if not api_key:
        return "LLM not available", "No OpenAI API key provided."
    openai.api_key = api_key
    prompt = f"""
You are a regulatory compliance expert. Review the following medical claim for compliance with {agency} regulations. 
Classify as 'Compliant', 'Non-Compliant', or 'Compliant with Evidence'.
If Non-Compliant, provide a brief explanation. If Compliant with Evidence, explain what evidence is present.

Medical Claim: "{text}"

Respond in this format:
Status: <Compliant/Non-Compliant/Compliant with Evidence>
Explanation: <short explanation>
"""
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=256,
            temperature=0.2,
        )
        content = response.choices[0].message.content.strip()
        # Parse response
        status_match = re.search(r"Status:\s*(.+)", content)
        explanation_match = re.search(r"Explanation:\s*(.+)", content)
        status = status_match.group(1).strip() if status_match else "Unknown"
        explanation = explanation_match.group(1).strip() if explanation_match else content
        return status, explanation
    except Exception as e:
        return "LLM error", str(e)

if __name__ == "__main__":
    sample = "According to a 2022 study in The Lancet, this drug guarantees 100% effectiveness in curing diabetes."
    status, details = check_compliance(sample, "FDA")
    print(f"Input: {sample}\nStatus: {status}")
    for v in details:
        print(f"Explanation: {v['explanation']} | Phrase: {v['phrase']}") 