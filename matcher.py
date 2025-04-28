from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import google.generativeai as genai
from config import GEMINI_API_KEY

genai.configure(api_key=GEMINI_API_KEY)
gemini_model = genai.GenerativeModel('gemini-pro')

def match_tender_to_profile_tfidf(tender_description, company_profile, threshold=0.5):
    if not tender_description or not company_profile:
        return None

    vectorizer = TfidfVectorizer()
    try:
        tfidf_matrix = vectorizer.fit_transform([tender_description, company_profile])
        cosine_sim = cosine_similarity(tfidf_matrix[0], tfidf_matrix[1])[0][0]
        return cosine_sim if cosine_sim >= threshold else None
    except Exception as e:
        print(f"Error during TF-IDF matching: {e}")
        return None

def match_tender_to_profile_gemini(tender_description, company_profile):
    prompt = f"""Determine the degree of relevance between the following tender description
    and the company's capabilities. Provide a score from 0 (not relevant) to 100 (highly relevant)
    and a brief explanation of your reasoning.

    Tender Description:
    {tender_description}

    Company Capabilities:
    {company_profile}

    Relevance Score (0-100):
    Reasoning:"""

    try:
        response = gemini_model.generate_content(prompt)
        if response.text:
            parts = response.text.split('\nReasoning:')
            score_str = parts[0].replace("Relevance Score (0-100):", "").strip()
            score = int(score_str) if score_str.isdigit() else 0
            reasoning = parts[1].strip() if len(parts) > 1 else ""
            return score, reasoning
        else:
            return 0, "No reasoning provided by Gemini."
    except Exception as e:
        print(f"Error during Gemini matching: {e}")
        return None, f"Error: {e}"

def match_tender_to_profile(tender_description, company_profile, use_gemini=False):
    if use_gemini and GEMINI_API_KEY != "YOUR_GEMINI_API_KEY_HERE":
        return match_tender_to_profile_gemini(tender_description, company_profile)
    else:
        return match_tender_to_profile_tfidf(tender_description, company_profile)

# You would need functions to process the raw tender data and company profile
# to extract the relevant text for the matching process.