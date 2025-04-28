import streamlit as st
import pandas as pd
from data_sources.cppp_scraper import fetch_cppp_tenders
from data_sources.gem_scraper import fetch_gem_tenders
from data_sources.state_scraper import fetch_state_tenders
from matching.matcher import match_tender_to_profile
from data_sources.utils import extract_text_from_pdf, extract_scope_from_url
from notifications.email_notifier import send_email_notification
from notifications.sms_notifier import send_sms_notification

st.title("Government Tender Tracker & Bid-Match Recommender")

@st.cache_data(ttl=3600)
def load_tenders():
    cppp_tenders = fetch_cppp_tenders()
    st.subheader("CPPP Tenders (Debug)")
    st.write(cppp_tenders)

    gem_tenders = fetch_gem_tenders()
    st.subheader("GeM Tenders (Debug)")
    st.write(gem_tenders)

    state_tenders = fetch_state_tenders()
    st.subheader("State Tenders (Debug)")
    st.write(state_tenders)

    all_tenders = cppp_tenders + gem_tenders + state_tenders
    return pd.DataFrame(all_tenders)

try:
    tenders_df = load_tenders()
    if not tenders_df.empty:
        st.subheader("Aggregated Tenders")
        st.dataframe(tenders_df)
    else:
        st.info("No tenders fetched from any source.")
except Exception as e:
    st.error(f"An error occurred while loading tenders: {e}")
    tenders_df = pd.DataFrame()

st.sidebar.header("Company Profile")
company_profile_text = st.sidebar.text_area("Enter your company's capabilities and services:")

use_gemini_matching = st.sidebar.checkbox("Use Gemini for Enhanced Matching (Requires API Key)")

if company_profile_text and not tenders_df.empty:
    st.subheader("Tender Matching")
    matched_tenders = []
    with st.spinner(f"Matching tenders using {'Gemini' if use_gemini_matching else 'TF-IDF'}..."):
        for index, row in tenders_df.iterrows():
            tender_details_text = ""
            if row['view_details_url']:
                tender_details_text = extract_scope_from_url(row['view_details_url'])

            if use_gemini_matching and GEMINI_API_KEY != "YOUR_GEMINI_API_KEY_HERE":
                gemini_result = match_tender_to_profile(tender_details_text, company_profile_text, use_gemini=True)
                if gemini_result:
                    match_score, reasoning = gemini_result
                    matched_tenders.append({**row.to_dict(), 'match_score': match_score / 100.0, 'reasoning': reasoning, 'matching_method': 'Gemini'})
            else:
                match_score = match_tender_to_profile(tender_details_text, company_profile_text, use_gemini=False)
                if match_score is not None:
                    matched_tenders.append({**row.to_dict(), 'match_score': match_score, 'matching_method': 'TF-IDF'})

    if matched_tenders:
        matched_df = pd.DataFrame(matched_tenders).sort_values(by='match_score', ascending=False)
        st.subheader("Matched Tenders")
        st.dataframe(matched_df)
        if 'reasoning' in matched_df.columns:
            st.subheader("Gemini Matching Reasoning")
            for index, row in matched_df.iterrows():
                st.write(f"**Tender:** {row['title']}")
                st.write(f"**Reasoning:** {row['reasoning']}")
                st.write("---")

        if st.sidebar.checkbox("Receive email alerts for high matches (Implementation Needed)"):
            st.warning("Email notification implementation is pending.")

        if st.sidebar.checkbox("Receive SMS alerts for high matches (Twilio Implementation Needed)"):
            st.warning("SMS notification implementation via Twilio is pending.")
    else:
        st.info("No tenders found that closely match your profile.")
elif not company_profile_text:
    st.info("Please enter your company's capabilities in the sidebar to see matching tenders.")
