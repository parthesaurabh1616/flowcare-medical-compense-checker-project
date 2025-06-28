import streamlit as st
import pandas as pd
from compliance_checker import check_compliance, llm_compliance_check
import io

st.title("Medical Text Compliance Checker")
st.write("Check if your medical claim is compliant with FDA, EMA, or HSA regulations.")

agency = st.selectbox("Select Regulatory Agency:", ["FDA", "EMA", "HSA"])
text = st.text_area("Enter medical claim or product statement:")

api_key = st.text_input("OpenAI API Key (for LLM second opinion, optional):", type="password")

if st.button("Check Compliance"):
    if text.strip():
        status, details = check_compliance(text, agency)
        st.markdown(f"**Status:** {'🟢 Compliant' if status == 'Compliant' else ('🟡 Compliant with Evidence' if status == 'Compliant with Evidence' else '🔴 Non-Compliant')}")
        if status.startswith('Compliant'):
            st.markdown(f"**Explanation:** {details[0]['explanation']}")
        else:
            st.markdown("**Detected Issues:**")
            for v in details:
                phrase = v['phrase']
                if phrase:
                    highlighted = text.replace(phrase, f'<span style=\"color:red;font-weight:bold\">{phrase}</span>')
                    st.markdown(f"- {v['explanation']}<br>Phrase: {highlighted}", unsafe_allow_html=True)
                else:
                    st.markdown(f"- {v['explanation']}")
        if st.button("Get LLM Second Opinion"):
            with st.spinner("Querying LLM..."):
                llm_status, llm_explanation = llm_compliance_check(text, agency, api_key)
                st.markdown(f"**LLM Status:** {llm_status}")
                st.markdown(f"**LLM Explanation:** {llm_explanation}")
    else:
        st.warning("Please enter a statement to check.")

st.markdown("---")
st.header("Bulk Compliance Check (CSV Upload)")

uploaded_file = st.file_uploader("Upload a CSV file with a 'statement' column:", type=["csv"])
if uploaded_file:
    df = pd.read_csv(uploaded_file)
    if 'statement' not in df.columns:
        st.error("CSV must have a 'statement' column.")
    else:
        use_llm_bulk = st.checkbox("Get LLM Second Opinion for All (may be slow and use OpenAI credits)")
        if use_llm_bulk and len(df) > 20:
            st.warning("You are about to send more than 20 LLM API calls. This may be slow and could incur costs.")
        results = []
        for s in df['statement']:
            status, details = check_compliance(str(s), agency)
            explanations = "; ".join([d['explanation'] for d in details])
            phrases = "; ".join([d['phrase'] for d in details if d['phrase']])
            llm_status, llm_explanation = ("", "")
            if use_llm_bulk and api_key:
                llm_status, llm_explanation = llm_compliance_check(str(s), agency, api_key)
            results.append({
                'statement': s,
                'status': status,
                'explanations': explanations,
                'offending_phrases': phrases,
                'llm_status': llm_status,
                'llm_explanation': llm_explanation
            })
        results_df = pd.DataFrame(results)
        st.subheader("Results Table")
        st.dataframe(results_df)
        # Summary
        st.subheader("Summary Dashboard")
        st.write(results_df['status'].value_counts())
        # Download
        csv = results_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download Results as CSV",
            data=csv,
            file_name="compliance_results.csv",
            mime="text/csv"
        ) 